import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Trash2, Pencil } from "lucide-react"; // Importe o ícone da caneta
import { UpdateCompraModal } from '../components/UpdateCompraModal'; // Importe o modal
import { useState } from "react";
import { usePessoas } from "@/hooks/usePessoas";
import { useCompras } from "@/hooks/useCompras";
import { format, parseISO } from "date-fns";

interface Comprador {
  id_pessoa: number; 
  nome: string;
}

interface Compra {
  id_compra: number;
  loc_entrega: string;
  valor: number;
  dt_emissao: string;
  dt_vencimento: string;
  dt_entrega?: string | null;
  dt_pagamento?: string | null;
  id_pessoa: number;
  nome_pessoa: string;
}

export default function CompraPage() {
  const [compradorSelecionado, setCompradorSelecionado] = useState<string | undefined>(undefined);
  const [enderecoCompra, setEnderecoCompra] = useState("");
  const [valorCompra, setValorCompra] = useState("");
  const [dataEmissao, setDataEmissao] = useState("");
  const [dataVencimento, setDataVencimento] = useState("");
  const [dataEntrega, setDataEntrega] = useState("");
  const [dataPagamento, setDataPagamento] = useState("");

  const { data: pessoa, isLoading: pessoaLoading } = usePessoas();
  
  const { data: compras, removeCompra, addCompra, updateCompra, isUpdating } = useCompras();

  const [isModalOpen, setIsModalOpen] = useState(false);
  const [compraSelecionada, setCompraSelecionada] = useState<Compra | null>(null);

  const handleAddCompra = async (e: React.FormEvent) => {
    e.preventDefault();

    // Validação: data de entrega antes da data de pagamento
    if (dataEntrega && dataPagamento && dataEntrega < dataPagamento) {
      alert("A data de entrega não pode ser anterior à data de pagamento.");
      return;
    }

    if (!enderecoCompra.trim()) {
      alert("Por favor, preencha o endereço.");
      return;
    }
    const novaCompra = {
      id_pessoa: compradorSelecionado,
      loc_entrega: enderecoCompra.trim(),
      valor: valorCompra.trim(),
      dt_emissao: dataEmissao,
      dt_vencimento: dataVencimento,
      dt_entrega: dataEntrega || null,
      dt_pagamento: dataPagamento || null,
    };
    await addCompra(novaCompra);

    setCompradorSelecionado(undefined);
    setEnderecoCompra("");
    setValorCompra("");
    setDataEmissao("");
    setDataVencimento("");
    setDataEntrega("");
    setDataPagamento("");
  };

  const handleOpenUpdateModal = (compra: Compra) => {
    setCompraSelecionada(compra);
    setIsModalOpen(true);
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
    setCompraSelecionada(null);
  };

  const handleSaveChanges = async (formData: Omit<Compra, 'id_compra' | 'nome_pessoa'>) => {
    if (!compraSelecionada) return;

    try {
      await updateCompra({ id: compraSelecionada.id_compra, data: formData });
      handleCloseModal();
    } catch (error) {
      console.error("Falha ao salvar:", error);
    }
  };

  return (
    <div className="flex flex-col flex-1 px-2 py-6 md:px-8 md:py-8">
      <div className="max-w-4xl mx-auto w-full">
        <h2 className="text-center text-2xl md:text-3xl font-bold mb-2">NOVA COMPRA</h2>
        <div className="h-3 w-full bg-[#891B14] rounded" />
        
        <form onSubmit={handleAddCompra} className="mt-6 bg-[#dddddd] rounded-2xl shadow-md pb-6 px-2 pt-5 space-y-4">
           <div className="bg-[#bdbdbd] rounded-lg py-3 px-3">
             <div className="space-y-3">
               <div className="space-y-1">
                 <div className="text-xs font-semibold">COMPRADOR</div>
                 <Select 
                   value={compradorSelecionado}
                   onValueChange={(idDoComprador) => setCompradorSelecionado(idDoComprador)}>
                   <SelectTrigger className="bg-white">
                     <SelectValue placeholder="Selecione um comprador" />
                   </SelectTrigger>
                   <SelectContent>
                     {!pessoaLoading && pessoa && pessoa.length === 0 && (
                       <div className="px-2 py-1 text-muted-foreground text-xs">Nenhuma pessoa</div>
                     )}
                     {!pessoaLoading && pessoa && pessoa.map((c: Comprador) => (
                       <SelectItem key={c.id_pessoa} value={String(c.id_pessoa)}>{c.nome}</SelectItem>
                     ))}
                   </SelectContent>
                 </Select>
               </div>
             </div>
           </div>

           <div className="space-y-1">
             <div className="text-xs font-semibold">LOCAL DE ENTREGA</div>
             <Input 
              value={enderecoCompra}
               onChange={(e) => setEnderecoCompra(e.target.value)}
               className="bg-white" 
               placeholder="Endereço completo para entrega" 
             />
           </div>

           <div className="space-y-1">
             <div className="text-xs font-semibold">VALOR DA COMPRA</div>
             <Input 
               value={valorCompra}
               onChange={(e) => setValorCompra(e.target.value)}
               className="bg-white" 
               type="number" step="0.01" 
               placeholder="0,00" 
             />
           </div>

           <div className="bg-[#bdbdbd] rounded-md py-3 px-3 space-y-3">
             <div className="text-center text-xs font-semibold mb-2">DATAS</div>
            
             <div className="flex gap-3">
               <div className="space-y-1 flex-1">
                 <div className="text-xs font-semibold">DATA DE EMISSÃO</div>
                 <Input
                   value={dataEmissao}
                  onChange={(e) => setDataEmissao(e.target.value)} 
                   className="bg-white" 
                   type="date" 
                 />
               </div>
               <div className="space-y-1 flex-1">
                 <div className="text-xs font-semibold">DATA DE VENCIMENTO</div>
                 <Input 
                   value={dataVencimento}
                   onChange={(e) => setDataVencimento(e.target.value)}
                   className="bg-white" 
                   type="date" 
                 />
               </div>
             </div>
            
             <div className="flex gap-3">
               <div className="space-y-1 flex-1">
                 <div className="text-xs font-semibold">DATA DE ENTREGA</div>
                   <Input 
                     value={dataEntrega}
                     onChange={(e) => setDataEntrega(e.target.value)}
                     className="bg-white" 
                     type="date" 
                   />
                 <div className="text-xs text-gray-600">Opcional</div>
               </div>
               <div className="space-y-1 flex-1">
                 <div className="text-xs font-semibold">DATA DE PAGAMENTO</div>
                 <Input
                   value={dataPagamento}
                   onChange={(e) => setDataPagamento(e.target.value)}
                   className="bg-white" 
                   type="date" 
                 />
                 <div className="text-xs text-gray-600">Opcional</div>
               </div>
             </div>
           </div>
          
           <div className="flex gap-4 mt-6 w-full justify-center">
             <Button 
               type="submit" 
               className="bg-[#d73f38] hover:bg-[#a12721] text-white font-semibold text-lg px-8">
               SALVAR
             </Button>
             <Button type="button" variant="secondary" className="bg-gray-500 hover:bg-gray-700 text-white font-semibold text-lg px-8">CANCELAR</Button>
           </div>
        </form>
        
        {/* Tabela de Compras */}
        <div className="mt-8 rounded-xl overflow-hidden bg-[#dddddd]">
          <table className="w-full text-sm">
            <thead className="text-left">
              <tr className="bg-[#bdbdbd]">
                <th className="py-2 px-3">ID</th>
                <th className="py-2 px-3">COMPRADOR</th>
                <th className="py-2 px-3">LOCAL DE ENTREGA</th>
                <th className="py-2 px-3">VALOR</th>
                <th className="py-2 px-3">VENCIMENTO</th>
                <th className="py-2 px-3 text-center">AÇÕES</th> {/* Nova coluna de ações */}
              </tr>
            </thead>
            <tbody>
              {compras?.map((compra: Compra) => (
                <tr key={compra.id_compra} className="border-b last:border-b-0">
                  <td className="py-2 px-3">{compra.id_compra}</td>
                  <td className="py-2 px-3">{compra.nome_pessoa}</td>
                  <td className="py-2 px-3">{compra.loc_entrega}</td>
                  <td className="py-2 px-3">R$ {compra.valor.toFixed(2)}</td>
                  <td className="py-2 px-3">{compra.dt_vencimento ? format(parseISO(compra.dt_vencimento), 'dd/MM/yyyy') : ''}</td>
                  <td className="py-2 px-3 flex gap-2 justify-center items-center">
                    <button onClick={() => handleOpenUpdateModal(compra)} title="Editar" className="hover:text-blue-600 p-1">
                      <Pencil size={18}/>
                    </button>
                    <button onClick={() => removeCompra(compra.id_compra)} title="Excluir" className="hover:text-[#891B14] p-1">
                      <Trash2 size={18}/>
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {isModalOpen && compraSelecionada && (
        <UpdateCompraModal
          compra={compraSelecionada}
          pessoas={pessoa || []} 
          onClose={handleCloseModal}
          onSave={handleSaveChanges}
          isUpdating={isUpdating}
        />
      )}
    </div>
  );
}