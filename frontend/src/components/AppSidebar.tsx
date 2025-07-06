//Barra de navegação que fica na lateral da tela

import { Link, useLocation } from "react-router-dom";
import { Menu } from "lucide-react";

//array com os itens e suas respectivas rotas
const menuItems = [
  { label: "Novo Orçamento", to: "/orcamento" },
  { label: "Agenda de Serviços", to: "/agenda" },
  { label: "Estoque", to: "/estoque" },
];
//Função que gera a side bar
export default function AppSidebar() {
  const location = useLocation();
  return (
    //70 px no mobile, 192px no desktop
    <nav className="min-h-screen w-[70px] md:w-48 bg-[#891B14] flex flex-col items-center pt-3">
      <div className="flex flex-col items-center w-full">
        {/* botão mobile, ícone de menu que só aparece no mobile */}
        <button className="mb-8 p-2 md:hidden">
          <Menu size={28} color="#fff" />
        </button>
        {/* Aqui é pra navegar pela sidebar, usa o location pra ver a rota atual e se já estiver nela, o botao fica com bg branco, se não continua com bg vermelho e com hover mais claro */}
        {menuItems.map((item) => (
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
