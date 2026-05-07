import { dashboardSnapshot } from '../data/mock';
import { DashboardSnapshot } from './types';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost/api/v1';

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      'Content-Type': 'application/json',
      ...(init?.headers ?? {}),
    },
    ...init,
  });

  if (!response.ok) {
    throw new Error(`Request failed with status ${response.status}`);
  }

  return response.json() as Promise<T>;
}

export async function loadDashboardSnapshot(): Promise<DashboardSnapshot> {
  try {
    return await request<DashboardSnapshot>('/metrics/dashboard');
  } catch {
    return dashboardSnapshot;
  }
}

export async function submitAnalysis(text: string, workspaceId?: string) {
  return request('/analysis/text', {
    method: 'POST',
    body: JSON.stringify({ text, workspace_id: workspaceId }),
  });
}
