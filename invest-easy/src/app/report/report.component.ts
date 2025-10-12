import { Component, OnInit, ElementRef, inject, viewChild, signal, effect, AfterViewChecked, AfterViewInit } from '@angular/core';

import { FormsModule } from '@angular/forms';
import { CardModule } from 'primeng/card';
import { ButtonModule } from 'primeng/button';
import { TableModule } from 'primeng/table';
import { RouterModule, ActivatedRoute } from '@angular/router';
import { TopNavigationComponent } from '../shared/top-navigation/top-navigation.component';
import { marked } from 'marked';
import { SseClient } from 'ngx-sse-client';

@Component({
  selector: 'app-report',
  standalone: true,
  templateUrl: './report.component.html',
  styleUrls: ['./report.component.scss'],
  imports: [
    FormsModule,
    CardModule,
    ButtonModule,
    TableModule,
    RouterModule,
    TopNavigationComponent
  ]
})
export class ReportComponent implements OnInit, AfterViewInit {
  private route = inject(ActivatedRoute);
  private sseClient = inject(SseClient);

  // Signal-based state
  reportContent = signal('');
  renderedContent = signal('');
  verboseContent = signal('');
  loading = signal(false);
  code = signal<string | null>(null);
  isVerboseExpanded = signal(false);
  private verboseContentChanged = signal(false);
  readonly verboseContentElement = viewChild.required<ElementRef>('verboseContentDiv');

  ngOnInit(): void {
    this.route.queryParams.subscribe(params => {
      const codeParam = params['code'];
      if (codeParam) {
        this.code.set(codeParam);
        this.generateReport();
      }
    });
  }

  ngAfterViewInit(): void {
  //   effect(() => {
  //     if (this.verboseContentChanged() && this.verboseContentElement()) {
  //       this.scrollToBottom();
  //     }
  //   })
  }

  private scrollToBottom(): void {
    try {
      const element = this.verboseContentElement().nativeElement;
      element.scrollTop = element.scrollHeight;
    } catch (err) {
      console.error('Error scrolling to bottom:', err);
    }
  }

  async generateReport(): Promise<void> {
    if (!this.code()) {
      console.error('No report code provided');
      return;
    }

    this.loading.update(x => true);
    this.reportContent.update(x => '');
    this.renderedContent.update(x => '');
    this.verboseContent.update(x => '');
    let finalContent = false;

    this.sseClient.stream(`reports/generate/${this.code()}`, { keepAlive: false, reconnectionDelay: 1_000, responseType: 'event' }, {}, 'GET').subscribe(async (event) => {
      if (event.type === 'error') {
        const errorEvent = event as ErrorEvent;
        console.error(errorEvent.error, errorEvent.message);
        this.loading.update(x => false);
        const errorMsg = '报告生成失败，请稍后重试。';
        this.reportContent.update(x => errorMsg);
        this.renderedContent.update(x => errorMsg);
      } else {
        const messageEvent = event as MessageEvent<string>;
        if (messageEvent.data.trim() == ('[[Final Answer Start]]')) {
          this.reportContent.update(x => "");
          finalContent = true;
        } else if (messageEvent.data.trim() == ('[[Final Answer End]]')) {
          const renderResult = await this.renderMarkdown(this.reportContent());
          this.renderedContent.update(x => renderResult);
          finalContent = false;
        } else if (messageEvent.data.trimStart().startsWith("[工具调用]")) {
          this.verboseContent.update(content => content + "\n" + messageEvent.data + "\n");
          this.verboseContentChanged.update(x => true);
        } else {
          if (messageEvent.data.trim() == "") {
            this.verboseContent.update(content => content + "\n\n");
            this.verboseContentChanged.update(x => true);
          } else {
            if (finalContent) {
              this.reportContent.update(content => content + messageEvent.data + "\n\n");
            } else {
              this.verboseContent.update(content => content + messageEvent.data);
              this.verboseContentChanged.update(x => true);
            }
          }
        }
        this.loading.update(x => false);
      }
    });
  }

  private async renderMarkdown(content: string): Promise<string> {
    try {
      // 配置 marked 选项
      marked.setOptions({
        breaks: true, // 将换行符转换为 <br>
        gfm: true,    // 启用 GitHub Flavored Markdown
      });

      return await marked.parse(content);
    } catch (error) {
      console.error('Error rendering markdown:', error);
      return content; // 如果渲染失败，返回原始内容
    }
  }
}
