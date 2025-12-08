#!/bin/bash
# ========================================================================
# PROJECT DETECTION SCRIPT
# ========================================================================
# Purpose: Detect current project from pwd for auto-savepoint routing
# Usage: ./detect_project.sh
# Output: project_type|savepoint_dir|git_push|port
# ========================================================================

# Get current working directory
CWD=$(pwd)

# Pattern matching (check most specific first to avoid false matches)
if [[ "$CWD" =~ /v15-presentation$ ]]; then
    # V15-Presentation: Active development project
    PROJECT_TYPE="v15-presentation"
    SAVEPOINT_DIR="/Users/admin/Documents/claudecode/workspaces/enterprise-ai-support/apps/v15-presentation"
    GIT_PUSH="YES"
    PORT="3016"

elif [[ "$CWD" =~ /tweakcn-clone-IT3$ ]]; then
    # atc.ds (IT3): Active development project
    PROJECT_TYPE="atc-ds"
    SAVEPOINT_DIR="/Users/admin/Documents/claudecode/workspaces/auzmor/apps/tweakcn-clone-IT3"
    GIT_PUSH="YES"
    PORT="3003"

elif [[ "$CWD" =~ /justice-league-missions ]]; then
    # Justice League Missions: Documentation/mission tracking
    PROJECT_TYPE="justice-league"
    SAVEPOINT_DIR="/Users/admin/Documents/claudecode/justice-league-missions"
    GIT_PUSH="YES"
    PORT="null"

elif [[ "$CWD" =~ /v14-production$ ]]; then
    # V14-Production: Stable baseline - DO NOT PUSH
    PROJECT_TYPE="v14-production"
    SAVEPOINT_DIR="/Users/admin/Documents/claudecode/workspaces/enterprise-ai-support/apps/v14-production"
    GIT_PUSH="NO"
    PORT="3014"

else
    # Unknown project: Global fallback for safety
    PROJECT_TYPE="unknown"
    SAVEPOINT_DIR="/Users/admin/Documents/claudecode/justice-league-missions"
    GIT_PUSH="NO"
    PORT="null"
fi

# Output result (pipe-separated for easy parsing)
echo "${PROJECT_TYPE}|${SAVEPOINT_DIR}|${GIT_PUSH}|${PORT}"

# Comments for Justice League agents:
# - v15-presentation: Active Next.js app, push to Git, Vercel MANUAL only
# - atc.ds: Active design system, push to Git, Vercel MANUAL only
# - justice-league: Mission docs, push to Git, NO Vercel (not a web app)
# - v14-production: STABLE BASELINE - never push (reference only)
# - unknown: Safety fallback - saves to global, no Git operations
