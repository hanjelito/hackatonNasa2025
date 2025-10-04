src/
  assets/               # imgs, fuentes, estilos globales
  components/           # componentes UI reutilizables (botones, cards, modales)
  features/             # módulos de negocio (users, auth, products, etc.)
    users/
      components/       # componentes específicos de "users"
      pages/            # vistas/route components del feature
      composables/      # lógica reutilizable (useUserForm, useFetchUsers)
      services/         # llamadas API del feature
      types/            # tipos/modelos del feature
    ...
  pages/                # páginas generales (si no usas features)
  layouts/              # layouts (DefaultLayout, AuthLayout)
  composables/          # hooks globales (useDarkMode, useToast)
  stores/               # Pinia stores
  router/               # rutas
  services/             # APIs genéricas (http client, interceptors)
  types/                # tipos globales (Env, RouteMeta)
  utils/                # helpers puros (formatDate, debounce)
  styles/               # tailwind.css, variables, base.css
  app.vue
  main.ts