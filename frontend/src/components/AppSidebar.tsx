//Barra de navegação que fica na lateral da tela

import { Link, useLocation } from "react-router-dom";
import { Menu } from "lucide-react";
import { useAuth } from "../hooks/useAuth";

//array com os itens e suas respectivas rotas
const menuItems = [
  { label: "Nova Cobrança", to: "/cobranca" },
  { label: "Compra", to: "/compra" },
  { label: "Agenda de Serviços", to: "/agenda" },
  { label: "Pessoa", to: "/pessoa" },
  { label: "Empresa", to: "/empresa" },
  { label: "Estoque", to: "/estoque" },
  { label: "Dashboard", to: "/dashboard" },
];


//Função que gera a side bar
export default function AppSidebar() {
  const location = useLocation();
  const { user } = useAuth();

  const filteredMenuItems = menuItems.filter(item => {
    // Se não houver usuário logado, não mostra nenhum item
    if (!user) {
      return false;
    }
    console.log(user.tipo)
    // Se o item for "Agenda de Serviços", mostra somente para tipo 0
    // if (item.to === '/agenda') {
    //   return user.tipo === 0 || user.tipo === 1;
    // }

    // Para todos os outros itens, mostra somente para tipo 1
    return user.tipo === 0 || user.tipo ===1;
  });

  return (
    //70 px no mobile, 192px no desktop
    <nav className="min-h-screen w-[70px] md:w-48 bg-[#891B14] flex flex-col items-center pt-3">
      <div className="flex flex-col items-center w-full">
        {/* botão mobile, ícone de menu que só aparece no mobile */}
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
    </nav>
  );
}
