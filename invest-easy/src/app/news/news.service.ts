import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, of } from 'rxjs';
// import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class NewsService {
  private apiUrl = 'https://newsapi.org/v2/everything';

  constructor() {}

//   getMarketNews(): Observable<any> {
//     const params = {
//       q: 'finance OR stock OR market',
//       language: 'en',
//       sortBy: 'publishedAt',
//       pageSize: '10',
//       apiKey: environment.newsApiKey
//     };
//     return this.http.get(this.apiUrl, { params });
//   }

  getMarketNews(): Observable<any> {
    return of(news_json);
  }
}


const news_json = {
    "status": "ok",
    "totalResults": 153365,
    "articles": [
        {
            "source": {
                "id": null,
                "name": "Www.gov.uk"
            },
            "author": "Department for Science, Innovation and Technology",
            "title": "University spinouts to grow industries of the future with new government backing",
            "description": "Public sector is being primed to bring innovative ideas out of government labs and onto the market with £30 million backing and new guidance.",
            "url": "https://www.gov.uk/government/news/university-spinouts-to-grow-industries-of-the-future-with-new-government-backing",
            "urlToImage": "https://assets.publishing.service.gov.uk/media/681cbbace26cd2f713d870f3/s960_University-spinout_govuk-3.png",
            "publishedAt": "2025-05-08T23:01:00Z",
            "content": "<ul><li>4 of the UKs most exciting regional research clusters to grow their ideas into thriving companies and industries of tomorrow with £30 million government backing</li><li>£30 million awarded to… [+6829 chars]"
        },
        {
            "source": {
                "id": null,
                "name": "Www.gov.uk"
            },
            "author": "Government Office for Technology Transfer",
            "title": "Guidance: Knowledge Asset Commercialisation Guide",
            "description": "Guidance to support Public Sector Bodies commercialising their Knowledge Assets via routes such as direct sales, licensing, joint ventures, and spinouts.",
            "url": "https://www.gov.uk/government/publications/knowledge-asset-commercialisation-guide",
            "urlToImage": "https://www.gov.uk/assets/static/govuk-opengraph-image-03837e1cec82f217cf32514635a13c879b8c400ae3b1c207c5744411658c7635.png",
            "publishedAt": "2025-05-08T23:01:00Z",
            "content": "The Knowledge Asset Commercialisation Guide provides information about different Knowledge Assets commercialisation routes available. These include direct sales, licensing, joint ventures, and spinou… [+1109 chars]"
        },
        {
            "source": {
                "id": null,
                "name": "Www.gov.uk"
            },
            "author": "Government Office for Technology Transfer",
            "title": "Guidance: Knowledge Asset Spinouts Guide",
            "description": "Guidance supporting public sector bodies to create spinout companies.",
            "url": "https://www.gov.uk/government/publications/knowledge-asset-spinouts-guide",
            "urlToImage": "https://www.gov.uk/assets/static/govuk-opengraph-image-03837e1cec82f217cf32514635a13c879b8c400ae3b1c207c5744411658c7635.png",
            "publishedAt": "2025-05-08T23:01:00Z",
            "content": "The Knowledge Asset spinouts guide provides detailed information on the creation of spinout companies as a commercialisation route for Knowledge Assets (KAs).\r\nThis guidance is to support public sect… [+1123 chars]"
        },
        {
            "source": {
                "id": null,
                "name": "Bitcoinist"
            },
            "author": "Keshav Verma",
            "title": "$263 Million In Crypto Shorts Rekt As Bitcoin Closes In On $100,000",
            "description": "Data shows the cryptocurrency derivatives market has suffered a high amount of liquidations as Bitcoin and other assets have rallied. Bitcoin Is Close To Revisiting The $100,000 Mark After a pullback under $94,000 earlier in the week, Bitcoin has seen a rejuv…",
            "url": "https://bitcoinist.com/263-million-crypto-shorts-rekt-bitcoin-100000/",
            "urlToImage": "https://bitcoinist.com/wp-content/uploads/2025/05/btc_16ea1f.webp",
            "publishedAt": "2025-05-08T23:00:47Z",
            "content": "Data shows the cryptocurrency derivatives market has suffered a high amount of liquidations as Bitcoin and other assets have rallied.\r\nBitcoin Is Close To Revisiting The $100,000 Mark\r\nAfter a pullba… [+2756 chars]"
        },
        {
            "source": {
                "id": null,
                "name": "Dailyutahchronicle.com"
            },
            "author": "By Teetad Govitviwat, News Writer",
            "title": "Drinking with ‘No Consequence’",
            "description": "Instead of trying to be like Celsius or Red Bull with massive sponsorships and spectacles behind their brand, the student-made No Consequence was designed to be an energy drink that anyone can drink and enjoy at the core of its identity. Braeden Riley, an Ope…",
            "url": "https://dailyutahchronicle.com/2025/05/08/drinking-with-no-consequence/",
            "urlToImage": "https://dailyutahchronicle.com/wp-content/uploads/2025/04/IMG_1684.jpg",
            "publishedAt": "2025-05-08T23:00:29Z",
            "content": "Instead of trying to be like Celsius or Red Bull with massive sponsorships and spectacles behind their brand, the student-made No Consequence was designed to be an energy drink that anyone can drink … [+2831 chars]"
        },
        {
            "source": {
                "id": null,
                "name": "Legalinsurrection.com"
            },
            "author": "Mary Chastain",
            "title": "Report: FBI Opens Case Against Letitia James for Alleged Mortgage Fraud",
            "description": "President Donald Trump's administration referred James to the DOJ in mid-April.\nThe post Report: FBI Opens Case Against Letitia James for Alleged Mortgage Fraud first appeared on Le·gal In·sur·rec·tion.",
            "url": "https://legalinsurrection.com/2025/05/report-fbi-opens-case-against-letitia-james-for-alleged-mortgage-fraud/",
            "urlToImage": "https://legalinsurrection.com/wp-content/uploads/2023/06/Letitia-James-e1687902992361.jpg",
            "publishedAt": "2025-05-08T23:00:29Z",
            "content": "The Times Unionreported that the FBI and the U.S. Attorney’s Office in Albany opened a case against New York Attorney General Letitia James for alleged mortgage fraud.\r\nJames is a New York elected of… [+3393 chars]"
        },
        {
            "source": {
                "id": null,
                "name": "ZDNet"
            },
            "author": "Kerry Wan",
            "title": "Samsung confirms big durability upgrade for Galaxy S25 Edge - and it's mostly good news",
            "description": "The Samsung Galaxy S25 Edge is launching soon, and the company just teased another spec that you should care about.",
            "url": "https://www.zdnet.com/article/samsung-confirms-big-durability-upgrade-for-galaxy-s25-edge-and-its-mostly-good-news/",
            "urlToImage": "https://www.zdnet.com/a/img/resize/d00bc3986a04932f2c92253922d6594c82da0dcf/2025/03/03/59bcedfb-718a-4b94-8582-e6999528e51e/dsc04194.jpg?auto=webp&fit=crop&height=675&width=1200",
            "publishedAt": "2025-05-08T23:00:21Z",
            "content": "Kerry Wan/ZDNET\r\nHoney, wake up. The latest Samsung Galaxy S25 Edge news just dropped, and it's a big one for those with slippery hands. Ahead of the virtual Samsung Unpacked event on Monday, the Kor… [+4836 chars]"
        },
        {
            "source": {
                "id": null,
                "name": "Ambcrypto.com"
            },
            "author": "Benjamin Njiri",
            "title": "OCC greenlights banks to trade crypto on behalf of clients",
            "description": "OCC's clarification could further integrate the crypto sector with the traditional banking system.",
            "url": "https://ambcrypto.com/occ-greenlights-banks-to-trade-crypto-on-behalf-of-clients/",
            "urlToImage": "https://ambcrypto.com/wp-content/uploads/2025/05/OCC-crypto-WP-1000x600.jpg",
            "publishedAt": "2025-05-08T23:00:11Z",
            "content": "<ul><li>OCC clarified that U.S. banks could hold, trade, or let third parties handle clients crypto assets. </li><li>However, the permissible crypto activities must happen within applicable laws. </l… [+1837 chars]"
        },
        {
            "source": {
                "id": null,
                "name": "GlobeNewswire"
            },
            "author": "Oak Ridge Financial Services",
            "title": "Oak Ridge Financial Services, Inc. Announces First Quarter 2025 Results and 17% Increase in Quarterly Cash Dividend",
            "description": "OAK RIDGE, N.C., May 08, 2025 (GLOBE NEWSWIRE) -- Oak Ridge Financial Services, Inc. (“Oak Ridge”; or the “Company”) (OTCPink: BKOR), the parent company of Bank of Oak Ridge (the “Bank”), announced unaudited financial results for the first three months of 202…",
            "url": "https://www.globenewswire.com/news-release/2025/05/08/3077897/28967/en/Oak-Ridge-Financial-Services-Inc-Announces-First-Quarter-2025-Results-and-17-Increase-in-Quarterly-Cash-Dividend.html",
            "urlToImage": "https://ml.globenewswire.com/Resource/Download/e4767839-a300-43e0-9565-dd09cdfe6ba7",
            "publishedAt": "2025-05-08T23:00:00Z",
            "content": "OAK RIDGE, N.C., May 08, 2025 (GLOBE NEWSWIRE) -- Oak Ridge Financial Services, Inc. (Oak Ridge; or the Company) (OTCPink: BKOR), the parent company of Bank of Oak Ridge (the Bank), announced unaudit… [+28688 chars]"
        },
        {
            "source": {
                "id": null,
                "name": "The Star Online"
            },
            "author": "The Star Online",
            "title": "Zahid proposes boosting franchise sector",
            "description": "KUALA LUMPUR: Deputy Prime Minister Datuk Seri Dr Ahmad Zahid Hamidi has proposed three initiatives, including the Asean Franchise Accelerator Programme, to elevate Malaysia's franchise ecosystem. Read full story",
            "url": "https://www.thestar.com.my/news/nation/2025/05/09/zahid-proposes-boosting-franchise-sector",
            "urlToImage": "https://apicms.thestar.com.my/uploads/images/2025/05/09/3306320.JPG",
            "publishedAt": "2025-05-08T23:00:00Z",
            "content": "KUALA LUMPUR: Deputy Prime Minister Datuk Seri Dr Ahmad Zahid Hamidi has proposed three initiatives, including the Asean Franchise Accelerator Programme, to elevate Malaysias franchise ecosystem.\r\nHe… [+2170 chars]"
        }
    ]
}
