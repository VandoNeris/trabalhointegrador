import { Link, useLocation, useNavigate } from "react-router-dom";
import { LogOutIcon, Menu } from "lucide-react";
import { useAuth } from "../hooks/useAuth";

const menuItems = [
  { label: "Nova Cobrança", to: "/cobranca" },
  { label: "Compra", to: "/compra" },
  { label: "Agenda de Serviços", to: "/agenda" },
  { label: "Pessoa", to: "/pessoa" },
  { label: "Empresa", to: "/empresa" },
  { label: "Estoque", to: "/estoque" },
  { label: "Dashboard", to: "/dashboard" },
];

export default function AppSidebar() {
  const location = useLocation();
  const navigate = useNavigate(); // Hook para redirecionar o usuário
  
  const { user, logout } = useAuth();

  const handleLogout = () => {
    if (window.confirm("Você tem certeza que deseja sair?")) {
      logout(); // Limpa o estado e o token
      navigate("/login", { replace: true }); // Redireciona para a página de login
    }
  };

  const filteredMenuItems = menuItems.filter(item => {
    if (!user) return false;
    
    return user.tipo === 0 || user.tipo === 1;
  });

  return (
    <nav className="min-h-screen w-[70px] md:w-48 bg-[#891B14] flex flex-col items-center pt-3">
      <div className="flex flex-col w-full h-full">
        <div className="flex flex-col items-center w-full">
          <button className="mb-8 p-2 md:hidden">
            <Menu size={28} color="#fff" />
          </button>
          {filteredMenuItems.map((item) => (
            <Link
              key={item.to}
              to={item.to}
              className={`mb-2 w-[90%] px-4 py-3 rounded-md ${
                location.pathname === item.to
                  ? "bg-white text-[#891B14] font-semibold"
                  : "text-white hover:bg-[#ad3c36]"
              } text-lg text-center duration-100`}
            >
              {item.label}
            </Link>
          ))}
        </div>
        <div className="mt-auto mb-4 w-full flex justify-center">
          {user && ( 
            <button
              onClick={handleLogout}
              title="Logout"
              className="flex items-center justify-center gap-2 w-[90%] text-white hover:bg-[#ad3c36] p-3 rounded-md duration-100"
            >
              <LogOutIcon size={22} />
              <span className="hidden md:inline">Sair</span>
            </button>
          )}
        </div>
      </div>
    </nav>
  );
}