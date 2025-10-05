import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { CardModule } from 'primeng/card';
import { ButtonModule } from 'primeng/button';
import { TableModule } from 'primeng/table';
import { RouterModule, ActivatedRoute } from '@angular/router';
import { TopNavigationComponent } from '../shared/top-navigation/top-navigation.component';

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
export class ReportComponent implements OnInit {
  reports: any[] = [];
  loading = false;
  code: string | null = null;

  constructor(private route: ActivatedRoute) { }

  ngOnInit(): void {
    this.route.paramMap.subscribe(params => {
      const codeParam = params.get('code');
      if (codeParam) {
        this.code = codeParam;
      }
    });

    console.log('Extracted code parameter:', this.code);
    this.loadReports();
  }

  loadReports(): void {
    this.loading = true;
    // 模拟加载报告数据
    setTimeout(() => {
      this.reports = [
        {
          id: 1,
          title: '投资组合分析报告',
          date: '2025-01-05',
          type: '投资分析',
          status: '已完成'
        },
        {
          id: 2,
          title: '市场趋势分析',
          date: '2025-01-04',
          type: '市场分析',
          status: '已完成'
        },
        {
          id: 3,
          title: '风险评估报告',
          date: '2025-01-03',
          type: '风险评估',
          status: '进行中'
        }
      ];
      this.loading = false;
    }, 1000);
  }

  generateReport(): void {
    // 生成新报告的逻辑
    console.log('生成新报告');
  }

  viewReport(report: any): void {
    // 查看报告详情
    console.log('查看报告:', report);
  }

  downloadReport(report: any): void {
    // 下载报告
    console.log('下载报告:', report);
  }
}
