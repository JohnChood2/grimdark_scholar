#!/bin/bash

# Deployment script for Warhammer 40K Lore Assistant
# This script helps you deploy to GitHub Pages with a custom domain

set -e

echo "🚀 Warhammer 40K Lore Assistant Deployment Script"
echo "=================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if we're in the right directory
if [ ! -f "package.json" ] && [ ! -f "frontend/package.json" ]; then
    print_error "Please run this script from the project root directory"
    exit 1
fi

# Get user input for domain name
echo ""
print_status "Choose your domain name:"
echo "1. grimdark-scholar.github.io (Recommended)"
echo "2. warhammer40k-professor.github.io"
echo "3. wh40k-lore-master.github.io"
echo "4. lexicanum-ai.github.io"
echo "5. warhammer-lore-ai.github.io"
echo "6. Custom domain"
echo ""

read -p "Enter your choice (1-6): " choice

case $choice in
    1)
        DOMAIN="grimdark-scholar.github.io"
        ;;
    2)
        DOMAIN="warhammer40k-professor.github.io"
        ;;
    3)
        DOMAIN="wh40k-lore-master.github.io"
        ;;
    4)
        DOMAIN="lexicanum-ai.github.io"
        ;;
    5)
        DOMAIN="warhammer-lore-ai.github.io"
        ;;
    6)
        read -p "Enter your custom domain: " DOMAIN
        ;;
    *)
        print_error "Invalid choice. Using default domain."
        DOMAIN="grimdark-scholar.github.io"
        ;;
esac

print_status "Using domain: $DOMAIN"

# Update CNAME file
print_status "Updating CNAME file..."
echo "$DOMAIN" > frontend/public/CNAME
print_success "CNAME file updated"

# Update package.json homepage
print_status "Updating package.json homepage..."
if [ -f "frontend/package.json" ]; then
    # Use sed to update homepage in package.json
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        sed -i '' "s|\"homepage\": \".*\"|\"homepage\": \"https://$DOMAIN\"|" frontend/package.json
    else
        # Linux
        sed -i "s|\"homepage\": \".*\"|\"homepage\": \"https://$DOMAIN\"|" frontend/package.json
    fi
    print_success "Package.json updated"
fi

# Check if git is initialized
if [ ! -d ".git" ]; then
    print_status "Initializing git repository..."
    git init
    git branch -M main
    print_success "Git repository initialized"
fi

# Check if remote origin exists
if ! git remote get-url origin >/dev/null 2>&1; then
    print_warning "No remote origin found. You'll need to add your GitHub repository:"
    echo "git remote add origin https://github.com/YOUR_USERNAME/40K_LLM.git"
    echo ""
fi

# Build frontend
print_status "Building frontend..."
cd frontend
npm install
npm run build
cd ..
print_success "Frontend built successfully"

# Check if GitHub Actions workflow exists
if [ ! -f ".github/workflows/deploy.yml" ]; then
    print_warning "GitHub Actions workflow not found. Creating it..."
    mkdir -p .github/workflows
    # The workflow file should already exist from our setup
fi

# Create deployment instructions
cat > DEPLOYMENT_INSTRUCTIONS.md << EOF
# 🚀 Deployment Instructions

## Your Domain: $DOMAIN

### Step 1: Push to GitHub
\`\`\`bash
git add .
git commit -m "Deploy Warhammer 40K Lore Assistant"
git push origin main
\`\`\`

### Step 2: Enable GitHub Pages
1. Go to your repository on GitHub
2. Click "Settings" → "Pages"
3. Set source to "GitHub Actions"
4. Your site will be available at: https://$DOMAIN

### Step 3: Deploy Backend (Railway)
1. Go to [railway.app](https://railway.app)
2. Create new project from GitHub repo
3. Set root directory to \`backend\`
4. Add environment variables:
   - OPENAI_API_KEY=your_key_here
   - DATABASE_URL=sqlite:///./wh40k_lore.db

### Step 4: Update API URL
1. Get your Railway backend URL
2. Update \`.github/workflows/deploy.yml\` with your backend URL
3. Push changes to trigger redeployment

## 🎉 Your site will be live at: https://$DOMAIN
EOF

print_success "Deployment instructions created: DEPLOYMENT_INSTRUCTIONS.md"

# Final instructions
echo ""
print_success "🎉 Deployment setup complete!"
echo ""
print_status "Next steps:"
echo "1. Push your code to GitHub:"
echo "   git add ."
echo "   git commit -m 'Deploy Warhammer 40K Lore Assistant'"
echo "   git push origin main"
echo ""
echo "2. Enable GitHub Pages in your repository settings"
echo ""
print_status "Your site will be available at: https://$DOMAIN"
echo ""
print_warning "Don't forget to deploy your backend to Railway and update the API URL!"
echo ""
print_success "Happy deploying! 🚀"
