import { Component, OnInit, OnDestroy, ElementRef, ViewChild, AfterViewChecked } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { CardModule } from 'primeng/card';
import { ButtonModule } from 'primeng/button';
import { TableModule } from 'primeng/table';
import { RouterModule, ActivatedRoute } from '@angular/router';
import { HttpClient, HttpEventType } from '@angular/common/http';
import { TopNavigationComponent } from '../shared/top-navigation/top-navigation.component';
import { Subscription } from 'rxjs';
import { marked } from 'marked';
import { SseClient } from 'ngx-sse-client';

@Component({
  selector: 'app-report',
  standalone: true,
  templateUrl: './report.component.html',
  styleUrls: ['./report.component.scss'],
  imports: [
    CommonModule,
    FormsModule,
    CardModule,
    ButtonModule,
    TableModule,
    RouterModule,
    TopNavigationComponent
  ]
})
export class ReportComponent implements OnInit, OnDestroy, AfterViewChecked {
  reportContent: string = '';
  renderedContent: string = '';
  verboseContent: string = '';
  loading = false;
  code: string | null = null;
  isVerboseExpanded = false;
  private subscription: Subscription | null = null;
  private verboseContentChanged = false;

  @ViewChild('verboseContentDiv') verboseContentElement!: ElementRef;

  constructor(
    private route: ActivatedRoute,
    private http: HttpClient,
    private sseClient: SseClient
  ) { }

  ngOnInit(): void {
    this.route.paramMap.subscribe(params => {
      const codeParam = params.get('code');
      if (codeParam) {
        this.code = codeParam;
        this.generateReport();
      }
    });
  }

  ngOnDestroy(): void {
    if (this.subscription) {
      this.subscription.unsubscribe();
    }
  }

  ngAfterViewChecked(): void {
    if (this.verboseContentChanged && this.verboseContentElement) {
      this.scrollToBottom();
      this.verboseContentChanged = false;
    }
  }

  private scrollToBottom(): void {
    try {
      const element = this.verboseContentElement.nativeElement;
      element.scrollTop = element.scrollHeight;
    } catch (err) {
      console.error('Error scrolling to bottom:', err);
    }
  }

  async generateReport(): Promise<void> {
    if (!this.code) {
      console.error('No report code provided');
      return;
    }

    this.loading = true;
    this.reportContent = '';
    this.renderedContent = '';
    this.verboseContent = '';
    let finalContent = false;


    this.sseClient.stream(`reports/generate/${this.code}`, { keepAlive: false, reconnectionDelay: 1_000, responseType: 'event' }, {}, 'GET').subscribe(async (event) => {
      if (event.type === 'error') {
        const errorEvent = event as ErrorEvent;
        console.error(errorEvent.error, errorEvent.message);
        this.loading = false;
        this.reportContent = '报告生成失败，请稍后重试。';
        this.renderedContent = await this.renderMarkdown('报告生成失败，请稍后重试。');
      } else {
        const messageEvent = event as MessageEvent<string>;
        if (messageEvent.data.trim() == ('[[Final Answer Start]]')) {
          this.reportContent = "";
          finalContent = true;
        } else if (messageEvent.data.trim() == ('[[Final Answer End]]')) {
          this.renderedContent = await this.renderMarkdown(this.reportContent);
          finalContent = false;
        } else if (messageEvent.data.trimStart().startsWith("[工具调用]")) {
          this.verboseContent += "\n";
          this.verboseContent += messageEvent.data;
          this.verboseContent += "\n";
          this.verboseContentChanged = true;
        } else {
          if (messageEvent.data.trim() == "") {
            this.verboseContent += "\n\n";
            this.verboseContentChanged = true;
          } else {
            if (finalContent) {
              this.reportContent += messageEvent.data;
              this.reportContent += "\n\n";
            } else {
              this.verboseContent += messageEvent.data;
              this.verboseContentChanged = true;
            }
          }
        }
        this.loading = false;
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
