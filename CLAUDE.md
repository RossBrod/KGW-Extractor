# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build Commands
- AdminApp (React/TS): `cd AdminApp && npm run dev` - Start development server
- AdminApp (React/TS): `cd AdminApp && npm run build` - Build for production
- AdminApp (Express): `cd AdminApp && node server.js` - Run backend server
- Python: `python NewWay.py` - Run main processing pipeline
- Python: `python ProcessCases.py` - Process case files

## Lint & Test Commands
- AdminApp: `cd AdminApp && npm run lint` - Run ESLint for TypeScript/React
- No automated tests detected in the codebase

## Code Style Guidelines
- TypeScript: Use strict type checking, interfaces for complex types
- React: Follow React hooks linting rules, functional components
- Python: Use type hints, docstrings, structured error handling
- Imports: Group by standard library, third-party, local modules
- Naming: camelCase for JS/TS, snake_case for Python
- Error handling: Try/catch in TypeScript with type guards, try/except in Python
- Database: Use transactions with proper commit/rollback patterns
- Environment: Use conditional logic for local vs production settings