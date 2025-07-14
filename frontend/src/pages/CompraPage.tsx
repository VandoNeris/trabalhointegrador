
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { X, Plus, Trash2 } from "lucide-react";
import { useState } from "react";
import { usePessoas } from "@/hooks/usePessoas";
import { useCompras } from "@/hooks/useCompras";


export default function CompraPage() {

  const [compradorSelecionado, setCompradorSelecionado] = useState<string | undefined>(undefined);
  const [enderecoCompra, setEnderecoCompra] = useState("");
  const [valorCompra, setValorCompra] = useState("");
  const [dataEmissao, setDataEmissao] = useState("");
  const [dataVencimento, setDataVencimento] = useState("");
  const [dataEntrega, setDataEntrega] = useState("");
  const [dataPagamento, setDataPagamento] = useState("");
  const { data: pessoa, isLoading: pessoaLoading } = usePessoas();
  const { data: compras, removeCompra, addCompra } = useCompras();

  // Defina esta interface acima do seu componente
  interface Comprador {
    id_pessoa: number; // <-- Troque 'id' pelo nome correto da sua propriedade (ex: _id, compradorId)
    nome: string;
    // adicione outras propriedades se houver
  }



  const handleAddCompra = async (e: React.FormEvent) => {
    e.preventDefault();
    // 1. Validação para garantir que o nome não está vazio
    if (!enderecoCompra.trim()) {
      alert("Por favor, preencha o endereço.");
      return;
    }

    // 2. Monta o objeto com os dados dos estados
    const novaCompra = {
      id_pessoa: compradorSelecionado,
      loc_entrega: enderecoCompra.trim(),
      valor: valorCompra.trim(),
      dt_emissao: dataEmissao,
      dt_vencimento: dataVencimento,
      dt_entrega: dataEntrega,
      dt_pagamento: dataPagamento,
    };

    // 3. Chama a função do hook para adicionar a pessoa
    await addCompra(novaCompra);

    // 4. Limpa os campos do formulário após o sucesso
    setCompradorSelecionado(undefined);
    setEnderecoCompra("");
    setValorCompra("");
    setDataEmissao("");
    setDataVencimento("");
    setDataEntrega("");
    setDataPagamento("");
  };

  return (
    <div className="flex flex-col flex-1 px-2 py-6 md:px-8 md:py-8">
      <div className="max-w-4xl mx-auto w-full">
        <h2 className="text-center text-2xl md:text-3xl font-bold mb-2">NOVA COMPRA</h2>
        <div className="h-3 w-full bg-[#891B14] rounded" />
        
        {/* Form Container */}
        <form onSubmit={handleAddCompra} className="mt-6 bg-[#dddddd] rounded-2xl shadow-md pb-6 px-2 pt-5 space-y-4">
          
          {/* Comprador */}
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

          {/* Local de Entrega */}
          <div className="space-y-1">
            <div className="text-xs font-semibold">LOCAL DE ENTREGA</div>
            <Input 
             value={enderecoCompra}
              onChange={(e) => setEnderecoCompra(e.target.value)}
              className="bg-white" 
              placeholder="Endereço completo para entrega" 
            />
          </div>

          {/* Valor */}
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

          {/* Datas */}
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
          
          {/* Actions */}
          <div className="flex gap-4 mt-6 w-full justify-center">
            <Button 
              type="submit" 
              className="bg-[#d73f38] hover:bg-[#a12721] text-white font-semibold text-lg px-8">
              SALVAR
            </Button>
            <Button type="button" variant="secondary" className="bg-gray-500 hover:bg-gray-700 text-white font-semibold text-lg px-8">CANCELAR</Button>
          </div>
        </form>
        <div className="rounded-xl overflow-hidden bg-[#dddddd]">
          <table className="w-full text-sm">
            <thead>
              <tr className="bg-[#bdbdbd]">
                <th className="py-2 px-3">ID</th>
                <th className="py-2 px-3">COMPRADOR</th>
                <th className="py-2 px-3">LOCAL DE ENTREGA</th>
                <th className="py-2 px-3">VALOR</th>
                <th className="py-2 px-3">DATA DE PAGAMENTO</th>
                <th className="py-2 px-3">DATA DE VENCIMENTO</th>
              </tr>
            </thead>            
              <tbody>
              {compras?.map((compra) => (
                <tr key={compra.id_pessoa} className="border-b last:border-b-0 text-center">
                  <td className="py-2">{compra.id_compra}</td>
                  <td className="py-2">{compra.nome_pessoa}</td>
                  <td className="py-2">{compra.loc_entrega}</td>
                  <td className="py-2">{compra.valor}</td>
                  <td className="py-2">{compra.dt_pagamento}</td>
                  <td className="py-2">{compra.dt_vencimento}</td>
                  <td className="py-2 flex gap-2 justify-center items-center">
                    <button onClick={() => removeCompra(compra.id_compra)} title="Excluir" className="hover:text-[#891B14] p-1"><Trash2 size={18}/></button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}