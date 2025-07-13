// src/hooks/useAuth.ts
import { useState, useEffect } from 'react';
import { jwtDecode } from 'jwt-decode';

// Define a estrutura esperada do payload do nosso token
interface DecodedToken {
  sub: string;
  tipo: number; // Assumindo que o tipo de usuário vem no token
}

export function useAuth() {
  const [user, setUser] = useState<DecodedToken | null>(null);

  useEffect(() => {
    try {
      const token = localStorage.getItem('accessToken');
      if (token) {
        // Decodifica o token para acessar os dados (payload)
        const decodedToken = jwtDecode<DecodedToken>(token);
        setUser(decodedToken);
      }
    } catch (error) {
      console.error("Erro ao decodificar o token:", error);
      // O token pode ser inválido, então limpamos para evitar erros futuros
      localStorage.removeItem('accessToken');
      setUser(null);
    }
  }, []); // O array vazio faz com que rode apenas uma vez, quando o componente é montado

  return { user };
}