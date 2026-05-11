param(
    [string]$Branch = "feature/fastapi-production",
    [string]$Remote = "origin",
    [string]$RepoUrl = "https://github.com/Mdehteshamulhaque1/Social-Media-Sentiment-Analysis.git",
    [string]$CommitMsg = "Refactor: production-ready FastAPI backend, realtime, ML, Celery, monitoring, Docker, CI"
)

Set-StrictMode -Version Latest

if (-not (Test-Path .git)) {
    Write-Host ".git not found. Initializing repository..."
    git init
}

git checkout -B $Branch
git add .
try {
    git commit -m $CommitMsg
} catch {
    Write-Host "No changes to commit"
}

try {
    git remote remove $Remote -ErrorAction SilentlyContinue
} catch {
    # ignore
}
git remote add $Remote $RepoUrl

Write-Host "Pushing to $Remote $Branch"
git push -u $Remote $Branch

Write-Host "Done. If push fails, authenticate with Git (PAT or SSH) and re-run the script."
