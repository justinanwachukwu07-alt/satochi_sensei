import { create } from "zustand"
import { persist } from "zustand/middleware"

interface AuthState {
  address: string | null
  isAuthed: boolean
  setAddress: (address: string | null) => void
  logout: () => void
}

interface UIState {
  sidebarCollapsed: boolean
  toggleSidebar: () => void
  setSidebarCollapsed: (collapsed: boolean) => void
}

export const useAuthStore = create<AuthState>((set) => ({
  address: null,
  isAuthed: false,
  setAddress: (address) => set({ address, isAuthed: !!address }),
  logout: () => set({ address: null, isAuthed: false }),
}))

export const useUIStore = create<UIState>()(
  persist(
    (set) => ({
      sidebarCollapsed: false,
      toggleSidebar: () => set((state) => ({ sidebarCollapsed: !state.sidebarCollapsed })),
      setSidebarCollapsed: (collapsed) => set({ sidebarCollapsed: collapsed }),
    }),
    {
      name: "satoshi-sensei-ui",
    },
  ),
)
