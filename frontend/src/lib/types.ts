export type SentimentTone = 'positive' | 'neutral' | 'negative';

export interface MetricCardData {
  label: string;
  value: string;
  delta: string;
  tone: SentimentTone;
}

export interface AnalysisRow {
  id: string;
  source: string;
  sentiment: SentimentTone;
  confidence: number;
  keywords: string[];
  createdAt: string;
}

export interface DashboardSnapshot {
  metrics: MetricCardData[];
  recentAnalyses: AnalysisRow[];
  topKeywords: Array<{ label: string; value: number }>;
  trendSeries: Array<{ label: string; positive: number; negative: number; neutral: number }>;
  sentimentHeatmap: Array<Array<number>>;
  systemHealth: Array<{ label: string; status: 'healthy' | 'degraded' | 'warning'; value: string }>;
  insightSummary?: string;
}
