//Pagina de agendamento com base nas telas feitos no figma, com dados estáticos por enquanto
import { Button } from "@/components/ui/button";
import { Plus } from "lucide-react";

export default function AgendaPage() {
  return (
    <div className="flex flex-col flex-1 px-2 py-6 md:px-8 md:py-8">
      <div className="max-w-3xl mx-auto w-full">
        <div className="flex items-center justify-between">
          <h2 className="text-2xl md:text-3xl font-bold mb-3">Agenda de serviços</h2>
          <Button className="bg-[#8a1c14] hover:bg-[#b8271e] text-white font-semibold"><Plus className="mr-1" size={18}/> NOVO AGENDAMENTO</Button>
        </div>
        <div className="h-3 w-full bg-[#891B14] rounded mb-3" />

        {/* Filters */}
        <div className="flex flex-col md:flex-row gap-3 mb-3">
          <input placeholder="Pesquisar por cliente ou id" className="bg-[#dddddd] rounded px-3 py-2 w-full md:w-[220px]"/>
          <input placeholder="Período: 01/05 - 30/05/2025" className="bg-[#dddddd] rounded px-3 py-2 w-full md:w-[220px]"/>
          <input placeholder="Status: Todos" className="bg-[#dddddd] rounded px-3 py-2 w-full md:w-[180px]"/>
        </div>
        
        {/* Próximos Agendamentos */}
        <div className="bg-[#bdbdbd] rounded-md mt-2 mb-4">
          <div className="font-semibold text-xs uppercase py-2 px-3 tracking-wider">Próximos Agendamentos</div>
          <div className="bg-white rounded-lg shadow p-2 flex flex-col gap-1 mx-4 my-2">
            <div className="flex flex-row items-center justify-between">
              <span className="font-semibold">08:00 João Vitor de Carvalho</span>
              <span className="bg-yellow-300 text-yellow-900 text-xs px-3 py-1 rounded-full font-bold">Pendente</span>
            </div>
            <div className="text-xs text-gray-600 pb-1">Manutenção Preventiva</div>
            <div className="flex justify-end gap-4 text-sm">
              <button className="text-blue-800 underline">Editar</button>
              <button className="text-blue-800 underline">Ver</button>
              <button className="text-blue-800 underline">Concluir</button>
            </div>
          </div>
        </div>
        {/* Serviços Concluídos */}
        <div className="bg-[#bdbdbd] rounded-md">
          <div className="font-semibold text-xs uppercase py-2 px-3 tracking-wider">Serviços Concluídos</div>
          {/* 1st finished */}
          <div className="border mt-2 rounded-lg bg-white mx-4 mb-2 shadow">
            <div className="flex flex-row items-center justify-between px-3 pt-3">
              <span className="font-semibold">12:30 Luiz Gustavo Piuco Bazzotti</span>
              <span className="bg-red-400 text-white text-xs px-3 py-1 rounded-full font-bold">AGUARDANDO PAGAMENTO</span>
            </div>
            <div className="flex flex-row justify-between px-3">
              <span className="text-xs">Instalação</span>
              <span className="font-semibold text-xs">Descrição</span>
            </div>
            <div className="px-3 py-1 text-xs">
              Serviço de instalação de motor em maquina D51, realizado no município de chapecó
            </div>
            <div className="flex gap-4 px-3 pb-2 text-sm justify-end">
              <button className="text-blue-800 underline">Editar</button>
              <button className="text-blue-800 underline">Ver</button>
              <button className="text-blue-800 underline">Concluir</button>
            </div>
          </div>
          {/* 2nd finished */}
          <div className="border rounded-lg bg-white mx-4 mb-2 shadow">
            <div className="flex flex-row items-center justify-between px-3 pt-3">
              <span className="font-semibold">06:00 Sérgio Alfredo Ramos</span>
              <span className="bg-green-500 text-white text-xs px-3 py-1 rounded-full font-bold">CONCLUIDO</span>
            </div>
            <div className="flex flex-row justify-between px-3">
              <span className="text-xs">Manutenção corretiva</span>
              <span className="font-semibold text-xs">Descrição</span>
            </div>
            <div className="px-3 py-1 text-xs">
              Manutenção de uma retroescavadeira Randon, realizado no interior de Coronel Freitas
            </div>
            <div className="flex gap-4 px-3 pb-2 text-sm justify-end">
              <button className="text-blue-800 underline">Ver detalhes</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
