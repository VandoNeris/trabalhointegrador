import { Plus } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { useEmpresas } from "@/hooks/useEmpresas";
import { useState } from "react";


export default function EmpresaPage() {
  const { data: empresas, isLoading: EmpresaLoading, addEmpresa } = useEmpresas();

  const [nomeEmpresa, setNomeEmpresa] = useState("");
  const [enderecoEmpresa, setEnderecoEmpresa] = useState("");
  const [emailEmpresa, setEmailEmpresa] = useState("");
  const [telefoneEmpresa, setTelefoneEmpresa] = useState("");
  const [cnpjEmpresa, setCnpjEmpresa] = useState("");

  // Função para lidar com a adição de uma nova empresa
  const handleAddEmpresa = async () => {
    // 1. Validação para garantir que o nome não está vazio
    if (!nomeEmpresa.trim()) {
      alert("Por favor, preencha o nome.");
      return;
    }

    // 2. Monta o objeto com os dados dos estados
    const novaEmpresa = {
      tipo: true, 
      nome: nomeEmpresa.trim(),
      endereco: enderecoEmpresa.trim(),
      email: emailEmpresa.trim(),
      telefone: telefoneEmpresa.trim(),
      cnpj: cnpjEmpresa.trim(),
    };

    // 3. Chama a função do hook para adicionar a empresa
    await addEmpresa(novaEmpresa);

    // 4. Limpa os campos do formulário após o sucesso
    setNomeEmpresa("");
    setEnderecoEmpresa("");
    setEmailEmpresa("");
    setTelefoneEmpresa("");
    setCnpjEmpresa("");
  };

  return (
    <div className="flex flex-col flex-1 px-2 py-6 md:px-8 md:py-8">
      <div className="max-w-4xl mx-auto w-full">
        <h2 className="text-2xl md:text-3xl font-bold mb-3">Empresas</h2>
        <div className="h-3 w-full bg-[#891B14] rounded mb-3" />

        {/* --- Formulário de Cadastro --- */}
        <div className="flex flex-col gap-3 mb-4">
          <div className="flex flex-col md:flex-row gap-3">
            {/* Input de Nome com onChange */}
            <Input
              placeholder="Nome *"
              value={nomeEmpresa}
              onChange={(e) => setNomeEmpresa(e.target.value)}
              className="bg-[#dddddd] rounded px-3 py-2 w-full"
            />
            {/* Input de Endereço com onChange */}
            <Input
              placeholder="Endereço"
              value={enderecoEmpresa}
              onChange={(e) => setEnderecoEmpresa(e.target.value)}
              className="bg-[#dddddd] rounded px-3 py-2 w-full"
            />
          </div>
          <div className="flex flex-col md:flex-row gap-3">
            {/* Outros inputs com onChange */}
            <Input
              placeholder="Email"
              value={emailEmpresa}
              onChange={(e) => setEmailEmpresa(e.target.value)}
              className="bg-[#dddddd] rounded px-3 py-2 w-full"
            />
            <Input
              placeholder="Telefone"
              value={telefoneEmpresa}
              onChange={(e) => setTelefoneEmpresa(e.target.value)}
              className="bg-[#dddddd] rounded px-3 py-2 w-full"
            />
            <Input
              placeholder="CNPJ"
              value={cnpjEmpresa}
              onChange={(e) => setCnpjEmpresa(e.target.value)}
              className="bg-[#dddddd] rounded px-3 py-2 w-full"
            />
          </div>
          {/* Botão para adicionar */}
          <div className="flex justify-end">
            <Button
              type="button"
              onClick={handleAddEmpresa}
              disabled={!nomeEmpresa.trim()} // Desabilita se o nome estiver vazio
              className="bg-[#891B14] hover:bg-[#ad3c36] text-white font-semibold"
            >
              <Plus size={16} className="mr-2" />
              Adicionar Empresa
            </Button>
          </div>
        </div>
        
        {/* Tabela */}
        <div className="rounded-xl overflow-hidden bg-[#dddddd]">
          <table className="w-full text-sm">
            <thead>
              <tr className="bg-[#bdbdbd]">
                <th className="py-2 px-3">ID</th>
                <th className="py-2 px-3">NOME</th>
                <th className="py-2 px-3">ENDEREÇO</th>
                <th className="py-2 px-3">EMAIL</th>
                <th className="py-2 px-3">TELEFONE</th>
                <th className="py-2 px-3">CNPJ</th>
              </tr>
            </thead>            
              <tbody>
              {empresas?.map((empresa) => (
                <tr key={empresa.id_pessoa} className="border-b last:border-b-0 text-center">
                  <td className="py-2">{empresa.id_pessoa}</td>
                  <td className="py-2">{empresa.nome}</td>
                  <td className="py-2">{empresa.endereco}</td>
                  <td className="py-2">{empresa.email}</td>
                  <td className="py-2">{empresa.telefone}</td>
                  <td className="py-2">{empresa.cnpj}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}