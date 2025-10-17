# Frontend Documentation

## Structure

- `components/` - Reusable Vue components
  - `common/` - Generic components (Button, Input, etc.)
  - `layout/` - Layout components (Header, Footer, Sidebar)
  - `features/` - Feature-specific components
- `views/` - Page components
- `router/` - Vue Router configuration
- `store/` - Pinia store modules
- `services/` - API service layer
- `utils/` - Utility functions
- `composables/` - Vue 3 composables
- `assets/` - Static assets (images, styles)

## Best Practices

1. Use Composition API with `<script setup>`
2. Create composables for reusable logic
3. Keep components small and focused
4. Use Pinia for state management
5. Centralize API calls in services
