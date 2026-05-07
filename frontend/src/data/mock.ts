import { DashboardSnapshot } from '../lib/types';

export const dashboardSnapshot: DashboardSnapshot = {
  metrics: [
    { label: 'Analyses processed', value: '342,881', delta: '+18.4%', tone: 'positive' },
    { label: 'Realtime queue', value: '41', delta: '-12.1%', tone: 'neutral' },
    { label: 'Avg confidence', value: '92.8%', delta: '+4.3%', tone: 'positive' },
    { label: 'API error rate', value: '0.42%', delta: '-0.08%', tone: 'negative' },
  ],
  recentAnalyses: [
    { id: 'ana_901', source: 'X / campaign_summer', sentiment: 'positive', confidence: 0.94, keywords: ['launch', 'brand', 'conversion'], createdAt: '2m ago' },
    { id: 'ana_902', source: 'Reddit / product-thread', sentiment: 'negative', confidence: 0.88, keywords: ['pricing', 'delay', 'support'], createdAt: '5m ago' },
    { id: 'ana_903', source: 'LinkedIn / executive-post', sentiment: 'neutral', confidence: 0.76, keywords: ['growth', 'market', 'forecast'], createdAt: '9m ago' },
    { id: 'ana_904', source: 'CSV upload / july_leads', sentiment: 'positive', confidence: 0.91, keywords: ['demand', 'segment', 'intent'], createdAt: '15m ago' },
  ],
  topKeywords: [
    { label: 'launch', value: 92 },
    { label: 'support', value: 84 },
    { label: 'pricing', value: 78 },
    { label: 'growth', value: 73 },
    { label: 'brand', value: 69 },
  ],
  trendSeries: [
    { label: 'Mon', positive: 48, negative: 21, neutral: 31 },
    { label: 'Tue', positive: 56, negative: 18, neutral: 26 },
    { label: 'Wed', positive: 61, negative: 24, neutral: 19 },
    { label: 'Thu', positive: 67, negative: 17, neutral: 22 },
    { label: 'Fri', positive: 74, negative: 15, neutral: 18 },
    { label: 'Sat', positive: 69, negative: 19, neutral: 24 },
    { label: 'Sun', positive: 77, negative: 14, neutral: 21 },
  ],
  sentimentHeatmap: [
    [18, 22, 40, 58, 44, 35],
    [24, 28, 42, 60, 52, 41],
    [15, 19, 34, 49, 46, 32],
    [20, 25, 37, 57, 55, 39],
  ],
  systemHealth: [
    { label: 'FastAPI', status: 'healthy', value: '99.98%' },
    { label: 'Redis cache', status: 'healthy', value: '81% hit rate' },
    { label: 'Celery workers', status: 'warning', value: '2 queued jobs' },
    { label: 'PostgreSQL', status: 'healthy', value: '14 ms p95' },
  ],
};
