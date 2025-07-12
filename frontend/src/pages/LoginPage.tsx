import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { useNavigate } from "react-router-dom";

export default function LoginPage() {
  const [usuario, setUsuario] = useState("");
  const [senha, setSenha] = useState("");
  const navigate = useNavigate();

  const handleLogin = () => {
    if (!usuario.trim() || !senha.trim()) {
      alert("Por favor, preencha todos os campos.");
      return;
    }
    
    navigate("/");
  };

  const handleCadastro = () => {
    navigate("/cadastro");
  };

  return (
    <div className="min-h-screen bg-[#891B14] flex items-center justify-center px-4">
      <div className="bg-white rounded-xl p-8 w-full max-w-md shadow-lg">
        <div className="text-center mb-6">
          <h1 className="text-3xl font-bold text-[#891B14] mb-2">Login</h1>
          <div className="h-1 w-16 bg-[#891B14] rounded mx-auto" />
        </div>

        <div className="flex flex-col gap-4">
          <Input
            placeholder="Usuário *"
            value={usuario}
            onChange={(e) => setUsuario(e.target.value)}
            className="bg-[#dddddd] rounded px-3 py-2 w-full"
          />
          
          <Input
            type="password"
            placeholder="Senha *"
            value={senha}
            onChange={(e) => setSenha(e.target.value)}
            className="bg-[#dddddd] rounded px-3 py-2 w-full"
          />

          <Button
            onClick={handleLogin}
            disabled={!usuario.trim() || !senha.trim()}
            className="bg-[#891B14] hover:bg-[#ad3c36] text-white font-semibold py-2 mt-2"
          >
            Entrar
          </Button>

          <div className="text-center mt-4">
            <p className="text-sm text-gray-600 mb-2">
              Não possui uma conta?
            </p>
            <Button
              variant="outline"
              onClick={handleCadastro}
              className="border-[#891B14] text-[#891B14] hover:bg-[#891B14] hover:text-white"
            >
              Cadastrar-se
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
}