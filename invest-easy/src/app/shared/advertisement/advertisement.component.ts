import { Component, Input } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { TopNavigationComponent } from '../top-navigation/top-navigation.component';

@Component({
  selector: 'app-advertisement',
  templateUrl: './advertisement.component.html',
  styleUrls: ['./advertisement.component.scss'],
  imports: [TopNavigationComponent]
})
export class AdvertisementComponent {
  adType: string = '';

  adTitle: string = '';
  adDescription: string = '';
  adImage: string = '';

  private adMappings: { [key: string]: { title: string, description: string, image: string } } = {
    'Account opening / upgrade': {
      title: 'Premium Account',
      description: 'Upgrade to our premium account with exclusive benefits and higher interest rates.',
      image: '/card-and-coin-colour-2025.jpg'
    },
    'Debit cards': {
      title: 'New Debit Card',
      description: 'Get our latest debit card with contactless payments and cashback rewards.',
      image: '/finance-banner.jpg'
    },
    'Well+': {
      title: 'Well+ Program',
      description: 'Join our wellness program for health insurance discounts and rewards.',
      image: '/gift.jpeg'
    },
    'Insurance': {
      title: 'Comprehensive Insurance',
      description: 'Protect what matters with our range of insurance products.',
      image: '/shield-lock-colour-2025.jpg'
    },
    'Time Deposits': {
      title: 'High Yield Deposits',
      description: 'Lock in higher interest rates with our time deposit accounts.',
      image: '/invest.jpg'
    },
    'Credit cards & instalment plans': {
      title: 'Premium Credit Card',
      description: 'Enjoy exclusive benefits with our premium credit card.',
      image: '/global-markets-banner.jpg'
    },
    'Explore Investments': {
      title: 'Explore Investment Opportunities',
      description: 'Discover a world of investment options tailored to your financial goals and risk appetite.',
      image: '/250429-investors-navigation-promo-370x208.jpg'
    },
    'Loans': {
      title: 'Flexible Loan Options',
      description: 'Get the funds you need with competitive rates and flexible repayment terms.',
      image: '/global-trade-solutions-banner.jpg'
    },
    'MPF': {
      title: 'Mandatory Provident Fund',
      description: 'Plan for your retirement with our comprehensive MPF solutions.',
      image: '/our-markets-768x576.jpg'
    },
    'Mobile Cash Withdrawal': {
      title: 'Mobile Cash Withdrawal',
      description: 'Withdraw cash without your card using just your mobile phone.',
      image: '/250116-digital-banking-promo-768x576.jpg'
    },
    'Foreign exchange rates': {
      title: 'Competitive FX Rates',
      description: 'Get the best foreign exchange rates for your international transactions.',
      image: '/euromoney-awards-trade-digital-banner.jpg'
    },
    'Deposit rates': {
      title: 'Attractive Deposit Rates',
      description: 'Earn more with our competitive deposit interest rates.',
      image: '/financial-regulation-header.jpg'
    },
    'ESG Hub': {
      title: 'ESG Investing',
      description: 'Invest with purpose through our Environmental, Social and Governance focused products.',
      image: '/240326-purpose-strategy-and-values-768x576.jpg'
    },
    'Your Quests': {
      title: 'Complete Quests, Earn Rewards',
      description: 'Engage with our banking services and earn exciting rewards.',
      image: '/230413-hsbc-and-wealth-768x576.jpg'
    }
  };

  constructor(private router: Router, private route: ActivatedRoute) { }

  ngOnInit() {
    this.route.params.subscribe(pm => {
      this.adType = pm['adType'] || '';
      console.log(this.adType)

      if (this.adType && this.adMappings[this.adType]) {
        const ad = this.adMappings[this.adType];
        this.adTitle = ad.title;
        this.adDescription = ad.description;
        this.adImage = ad.image;
      }
    })
  }
}
