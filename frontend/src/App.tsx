
import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import AppSidebar from "./components/AppSidebar";
import CobrancaPage from "./pages/CobrancaPage";
import AgendaPage from "./pages/AgendaPage";
import EstoquePage from "./pages/EstoquePage";
import Index from "./pages/Index";
import NotFound from "./pages/NotFound";
import PessoaPage from "./pages/PessoaPage";
import EmpresaPage from "./pages/EmpresaPage";
import LoginPage from "./pages/LoginPage";
import CadastroPage from "./pages/CadastroPage";
import DashboardsPage from "./pages/DashboardsPage";
import CompraPage from "./pages/CompraPage";

const queryClient = new QueryClient();

const AppLayout = ({ children }: { children: React.ReactNode }) => (
  <div className="min-h-screen flex w-full">
    <AppSidebar />
    <div className="flex-1">{children}</div>
  </div>
);

const App = () => (
  <QueryClientProvider client={queryClient}>
    <TooltipProvider>
      <Toaster />
      <Sonner />
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Index />} />
          <Route
            path="/login"
            element={
                <LoginPage />
            }
          />
          <Route
            path="/cadastro"
            element={
                <CadastroPage />
            }
          />
          <Route
            path="/compra"
            element={
              <AppLayout>
                <CompraPage />
              </AppLayout>
            }
          />
          <Route
            path="/cobranca"
            element={
              <AppLayout>
                <CobrancaPage />
              </AppLayout>
            }
          />
          <Route
            path="/agenda"
            element={
              <AppLayout>
                <AgendaPage />
              </AppLayout>
            }
          />
          <Route
            path="/pessoa"
            element={
              <AppLayout>
                <PessoaPage />
              </AppLayout>
            }
          />
          <Route
            path="/empresa"
            element={
              <AppLayout>
                <EmpresaPage />
              </AppLayout>
            }
          />
          <Route
            path="/estoque"
            element={
              <AppLayout>
                <EstoquePage />
              </AppLayout>
            }
          />
          <Route
            path="/dashboard"
            element={
              <AppLayout>
                <DashboardsPage />
              </AppLayout>
            }
          />
          <Route path="*" element={<NotFound />} />
        </Routes>
      </BrowserRouter>
    </TooltipProvider>
  </QueryClientProvider>
);

export default App;
