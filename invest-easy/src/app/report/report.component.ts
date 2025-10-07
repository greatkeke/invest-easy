import { Component, OnInit, OnDestroy } from '@angular/core';
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
export class ReportComponent implements OnInit, OnDestroy {
  reportContent: string = '';
  renderedContent: string = '';
  loading = false;
  code: string | null = null;
  private subscription: Subscription | null = null;

  constructor(
    private route: ActivatedRoute,
    private http: HttpClient
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

  async generateReport(): Promise<void> {
    if (!this.code) {
      console.error('No report code provided');
      return;
    }

    this.loading = true;
    this.reportContent = '';
    this.renderedContent = '';

    // 调用后端API生成报告
    this.subscription = this.http.post(`reports/generate/${this.code}`, {}
    ).subscribe({
      next: async (event: any) => {
        this.reportContent = event.output;
        this.renderedContent = await this.renderMarkdown(event.output);
        this.loading = false;
      },
      error: async (error) => {
        this.loading = false;
        console.error('Error generating report:', error);
        this.reportContent = '报告生成失败，请稍后重试。';
        this.renderedContent = await this.renderMarkdown('报告生成失败，请稍后重试。');
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
