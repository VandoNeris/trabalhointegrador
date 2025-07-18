
// Tela inicial
import { useEffect } from "react";
import { useNavigate } from "react-router-dom";

const Index = () => {
  const navigate = useNavigate();
  useEffect(() => {
    // navigate("/cobranca", { replace: true });
    navigate("/login", { replace: true });
  }, [navigate]);
  return null;
};

export default Index;
