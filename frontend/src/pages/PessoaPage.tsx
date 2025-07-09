import { Plus } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { usePessoas } from "@/hooks/usePessoas";
import { useState } from "react";


export default function PessoaPage() {
  const { data: pessoas, isLoading: pessoaLoading, addPessoa } = usePessoas();

  const [nomePessoa, setNomePessoa] = useState("");
  const [enderecoPessoa, setEnderecoPessoa] = useState("");
  const [emailPessoa, setEmailPessoa] = useState("");
  const [telefonePessoa, setTelefonePessoa] = useState("");
  const [cpfPessoa, setCpfPessoa] = useState("");

  // Função para lidar com a adição de uma nova pessoa
  const handleAddPessoa = async () => {
    // 1. Validação para garantir que o nome não está vazio
    if (!nomePessoa.trim()) {
      alert("Por favor, preencha o nome.");
      return;
    }

    // 2. Monta o objeto com os dados dos estados
    const novaPessoa = {
      tipo: false, 
      nome: nomePessoa.trim(),
      endereco: enderecoPessoa.trim(),
      email: emailPessoa.trim(),
      telefone: telefonePessoa.trim(),
      cpf: cpfPessoa.trim(),
    };

    // 3. Chama a função do hook para adicionar a pessoa
    await addPessoa(novaPessoa);

    // 4. Limpa os campos do formulário após o sucesso
    setNomePessoa("");
    setEnderecoPessoa("");
    setEmailPessoa("");
    setTelefonePessoa("");
    setCpfPessoa("");
  };

  return (
    <div className="flex flex-col flex-1 px-2 py-6 md:px-8 md:py-8">
      <div className="max-w-4xl mx-auto w-full">
        <h2 className="text-2xl md:text-3xl font-bold mb-3">Pessoas</h2>
        <div className="h-3 w-full bg-[#891B14] rounded mb-3" />

        {/* --- Formulário de Cadastro --- */}
        <div className="flex flex-col gap-3 mb-4">
          <div className="flex flex-col md:flex-row gap-3">
            {/* Input de Nome com onChange */}
            <Input
              placeholder="Nome *"
              value={nomePessoa}
              onChange={(e) => setNomePessoa(e.target.value)}
              className="bg-[#dddddd] rounded px-3 py-2 w-full"
            />
            {/* Input de Endereço com onChange */}
            <Input
              placeholder="Endereço"
              value={enderecoPessoa}
              onChange={(e) => setEnderecoPessoa(e.target.value)}
              className="bg-[#dddddd] rounded px-3 py-2 w-full"
            />
          </div>
          <div className="flex flex-col md:flex-row gap-3">
            {/* Outros inputs com onChange */}
            <Input
              placeholder="Email"
              value={emailPessoa}
              onChange={(e) => setEmailPessoa(e.target.value)}
              className="bg-[#dddddd] rounded px-3 py-2 w-full"
            />
            <Input
              placeholder="Telefone"
              value={telefonePessoa}
              onChange={(e) => setTelefonePessoa(e.target.value)}
              className="bg-[#dddddd] rounded px-3 py-2 w-full"
            />
            <Input
              placeholder="CPF"
              value={cpfPessoa}
              onChange={(e) => setCpfPessoa(e.target.value)}
              className="bg-[#dddddd] rounded px-3 py-2 w-full"
            />
          </div>
          {/* Botão para adicionar */}
          <div className="flex justify-end">
            <Button
              type="button"
              onClick={handleAddPessoa}
              disabled={!nomePessoa.trim()} // Desabilita se o nome estiver vazio
              className="bg-[#891B14] hover:bg-[#ad3c36] text-white font-semibold"
            >
              <Plus size={16} className="mr-2" />
              Adicionar Pessoa
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
                <th className="py-2 px-3">CPF</th>
              </tr>
            </thead>            
              <tbody>
              {pessoas?.map((pessoa) => (
                <tr key={pessoa.id_pessoa} className="border-b last:border-b-0 text-center">
                  <td className="py-2">{pessoa.id_pessoa}</td>
                  <td className="py-2">{pessoa.nome}</td>
                  <td className="py-2">{pessoa.endereco}</td>
                  <td className="py-2">{pessoa.email}</td>
                  <td className="py-2">{pessoa.telefone}</td>
                  <td className="py-2">{pessoa.cpf}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}