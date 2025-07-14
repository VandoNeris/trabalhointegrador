// src/hooks/useAuth.ts
import { useState, useEffect, useCallback } from 'react';
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
        const decodedToken = jwtDecode<DecodedToken>(token);
        setUser(decodedToken);
      }
    } catch (error) {
      console.error("Erro ao decodificar o token:", error);
      localStorage.removeItem('accessToken');
      setUser(null);
    }
  }, []);

  const logout = useCallback(() => {
    console.log("Realizando logout...");
    // Remove o token do armazenamento local
    localStorage.removeItem('accessToken');
    // Limpa o estado do usuário na aplicação
    setUser(null);
  }, []); 

  return { user, logout };
}