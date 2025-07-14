import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { useNavigate } from "react-router-dom";
import { useUsuarios } from "@/hooks/useUsuarios";

export default function CadastroPage() {
  const { data: usuarios, isLoading: usuarioLoading, addUsuario } = useUsuarios();

  const [nome, setNome] = useState("");
  const [senha, setSenha] = useState("");
  const [confirmaSenha, setConfirmaSenha] = useState(""); 
  const navigate = useNavigate();

  const handleCadastro = async () => {
    // Validação de campos vazios
    if (!nome.trim() || !senha.trim() || !confirmaSenha.trim()) {
      alert("Por favor, preencha todos os campos.");
      return;
    }

    // Verificação do tamanho mínimo da senha
    if (senha.length < 6) {
      alert("A senha deve ter pelo menos 6 caracteres.");
      return;
    }

    // <-- 2. ADICIONADO: Verificação se as senhas coincidem
    if (senha !== confirmaSenha) {
      alert("As senhas não coincidem. Por favor, verifique.");
      return;
    }

    try {
        const novoUsuario = {
        tipo: false, 
        nome: nome.trim(),
        senha:senha.trim(),
        };
 
        const reponse = await addUsuario(novoUsuario);

        setNome("");
        setSenha("");
        setConfirmaSenha("");
        alert(reponse.message);
        navigate("/login");

    } catch (error) {
      alert("Ocorreu um erro de conexão. Verifique o console para mais detalhes.");
      console.error("Erro na chamada da API:", error);
    }
  };

  return (
    <div className="min-h-screen bg-[#891B14] flex items-center justify-center px-4">
      <div className="bg-white rounded-xl p-8 w-full max-w-md shadow-lg">
        <div className="text-center mb-6">
          <h1 className="text-3xl font-bold text-[#891B14] mb-2">Criar Conta</h1>
          <div className="h-1 w-16 bg-[#891B14] rounded mx-auto" />
        </div>

        <div className="flex flex-col gap-4">
          <Input
            placeholder="Nome de Usuário *"
            value={nome}
            onChange={(e) => setNome(e.target.value)}
            className="bg-[#dddddd] rounded px-3 py-2 w-full"
          />
          <Input
            type="password"
            placeholder="Senha *"
            value={senha}
            onChange={(e) => setSenha(e.target.value)}
            className="bg-[#dddddd] rounded px-3 py-2 w-full"
          />
          {/* 3. ADICIONADO: Campo para confirmar a senha --> */}
          <Input
            type="password"
            placeholder="Confirmar Senha *"
            value={confirmaSenha}
            onChange={(e) => setConfirmaSenha(e.target.value)}
            className="bg-[#dddddd] rounded px-3 py-2 w-full"
          />
          <Button
            onClick={handleCadastro}
            // A desativação do botão agora também verifica o novo campo
            disabled={!nome.trim() || !senha.trim() || !confirmaSenha.trim()}
            className="bg-[#891B14] hover:bg-[#ad3c36] text-white font-semibold py-2 mt-2"
          >
            Cadastrar
          </Button>
          
          <div className="text-center mt-4">
            <p className="text-sm text-gray-600 mb-2">
              Já possui uma conta?
            </p>
            <Button
              variant="outline"
              onClick={() => navigate('/login')}
              className="border-[#891B14] text-[#891B14] hover:bg-[#891B14] hover:text-white"
            >
              Fazer Login
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
}