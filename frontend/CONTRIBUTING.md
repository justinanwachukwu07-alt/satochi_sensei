# Contributing to Satoshi Sensei

Thank you for your interest in contributing to Satoshi Sensei! This document provides guidelines and information for contributors.

## 🚀 Getting Started

### Prerequisites
- Node.js 18+
- Git
- A code editor (VS Code recommended)
- Basic knowledge of React, TypeScript, and Next.js

### Development Setup

1. **Fork and clone the repository**
   \`\`\`bash
   git clone https://github.com/your-username/satoshi-sensei.git
   cd satoshi-sensei
   \`\`\`

2. **Install dependencies**
   \`\`\`bash
   npm install
   \`\`\`

3. **Set up environment variables**
   \`\`\`bash
   cp .env.example .env.local
   \`\`\`

4. **Start the development server**
   \`\`\`bash
   npm run dev
   \`\`\`

## 📋 Development Guidelines

### Code Style
- Use **TypeScript** for all new code
- Follow **ESLint** and **Prettier** configurations
- Use **Conventional Commits** for commit messages
- Write **JSDoc** comments for components and functions
- Maintain **test coverage** for new features

### Component Guidelines
- Use **functional components** with hooks
- Implement **proper TypeScript interfaces**
- Follow **shadcn/ui** patterns for UI components
- Use **Tailwind CSS** for styling
- Implement **responsive design** (mobile-first)

### State Management
- Use **Zustand** for global state
- Keep **local state** in components when possible
- Use **React Query** for server state
- Implement **proper error handling**

## 🐛 Bug Reports

When reporting bugs, please include:
- **Clear description** of the issue
- **Steps to reproduce** the problem
- **Expected vs actual behavior**
- **Screenshots** if applicable
- **Environment details** (OS, browser, Node version)

## ✨ Feature Requests

For new features:
- **Check existing issues** first
- **Describe the use case** clearly
- **Explain the expected behavior**
- **Consider implementation complexity**
- **Discuss with maintainers** before large changes

## 🔄 Pull Request Process

1. **Create a feature branch**
   \`\`\`bash
   git checkout -b feature/your-feature-name
   \`\`\`

2. **Make your changes**
   - Write clean, documented code
   - Add tests for new functionality
   - Update documentation if needed

3. **Test your changes**
   \`\`\`bash
   npm run test
   npm run lint
   npm run type-check
   \`\`\`

4. **Commit with conventional format**
   \`\`\`bash
   git commit -m "feat: add new trading indicator"
   git commit -m "fix: resolve wallet connection issue"
   git commit -m "docs: update API documentation"
   \`\`\`

5. **Push and create PR**
   \`\`\`bash
   git push origin feature/your-feature-name
   \`\`\`

### PR Requirements
- **Clear title** and description
- **Link related issues**
- **Include screenshots** for UI changes
- **Pass all CI checks**
- **Get approval** from maintainers

## 🧪 Testing

### Running Tests
\`\`\`bash
# Run all tests
npm run test

# Run tests in watch mode
npm run test:watch

# Generate coverage report
npm run test:coverage
\`\`\`

### Writing Tests
- **Unit tests** for utilities and hooks
- **Component tests** for UI components
- **Integration tests** for complex flows
- **E2E tests** for critical user journeys

## 📚 Documentation

### Code Documentation
- **JSDoc comments** for all public functions
- **TypeScript interfaces** for all data structures
- **README updates** for new features
- **Inline comments** for complex logic

### API Documentation
- **OpenAPI specs** for backend endpoints
- **Example requests/responses**
- **Error code documentation**
- **Authentication flow diagrams**

## 🔐 Security

### Security Guidelines
- **Never commit** sensitive data
- **Validate all inputs** on client and server
- **Use HTTPS** for all external requests
- **Follow OWASP** security practices
- **Report security issues** privately

### Wallet Security
- **Non-custodial** approach only
- **Secure transaction signing**
- **Proper nonce handling**
- **Rate limiting** for API calls

## 🎨 Design Guidelines

### UI/UX Standards
- Follow **Neon Bitcoin Noir** aesthetic
- Use **Bitcoin orange** (#F7931A) and **Stacks purple** (#5546FF)
- Maintain **high contrast** for accessibility
- Implement **smooth animations** with Framer Motion
- Ensure **responsive design** across all devices

### Accessibility
- **WCAG 2.1 AA** compliance
- **Keyboard navigation** support
- **Screen reader** compatibility
- **Color contrast** requirements
- **Focus indicators** for all interactive elements

## 📞 Communication

### Getting Help
- **GitHub Discussions** for questions
- **Discord** for real-time chat
- **GitHub Issues** for bugs and features
- **Email** for security concerns

### Community Guidelines
- Be **respectful** and **inclusive**
- **Help others** learn and grow
- **Share knowledge** and experiences
- **Follow code of conduct**

## 📄 License

By contributing to Satoshi Sensei, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to Satoshi Sensei! 🚀
