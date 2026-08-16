# JavaScript to TypeScript Migration Project

Progressive migration of JS/JSX files to TypeScript in Apache Superset frontend.

**Status: complete for application code.** `superset-frontend/src` contains no
`.js`/`.jsx` files, and only a handful remain across `packages` and `plugins` —
all of them Yeoman generator templates, Jest config and CommonJS mocks that are
intentionally left as JavaScript. This playbook is kept for reference and for
any stray JavaScript reintroduced in the future.

## 📁 Project Documentation

- **[AGENT.md](./AGENT.md)** - Complete technical migration guide for agents (includes type reference, patterns, validation)
- **[COORDINATOR.md](./COORDINATOR.md)** - Strategic workflow for coordinators (file selection, task management, integration)

## 🎯 Quick Start

**For Agents:** Read [AGENT.md](./AGENT.md) for complete migration instructions
**For Coordinators:** Read [COORDINATOR.md](./COORDINATOR.md) for workflow and [AGENT.md](./AGENT.md) for supervision

**Command:** `/js-to-ts <filename>` - See [../../commands/js-to-ts.md](../../commands/js-to-ts.md)

## 📊 Migration Progress

**Strategy**: Leaf-first migration with dependency-aware coordination.

Application code is fully migrated. To see what JavaScript is left:

```bash
find superset-frontend/src superset-frontend/packages superset-frontend/plugins \
  -name '*.js' -o -name '*.jsx' | grep -v node_modules
```

The remaining files are generator templates, Jest configuration and CommonJS
mocks; they are out of scope and should stay as JavaScript.

**Per-File Gates** (for any future migration):
- ✅ `npm run type` passes after each migration
- ✅ Zero `any` types introduced
- ✅ All imports properly typed
- ✅ Types filed in correct hierarchy
- ✅ Test coverage (created where missing)

---

*This is a claudette-managed progressive refactor. All documentation and coordination resources are organized under `.claude/projects/js-to-ts/`*
