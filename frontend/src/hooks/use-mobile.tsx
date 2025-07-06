//função do react para tela pequena(mobile)

import * as React from "react"

//abaixo de 768 é considerado mobile
const MOBILE_BREAKPOINT = 768
//pega informação se o usuario é mobile ou não, começa undefined como padrão pois não se sabe inicialmente o tamanho da tela
export function useIsMobile() {
  const [isMobile, setIsMobile] = React.useState<boolean | undefined>(undefined)

  React.useEffect(() => {
    //checa se é menor que 768px
    const mql = window.matchMedia(`(max-width: ${MOBILE_BREAKPOINT - 1}px)`)
    //pra atualizar a tela sempre que mudar
    const onChange = () => {
      //seta o tamanho da tela com base na largura atual
      setIsMobile(window.innerWidth < MOBILE_BREAKPOINT)
    }

    mql.addEventListener("change", onChange)
    setIsMobile(window.innerWidth < MOBILE_BREAKPOINT)
    return () => mql.removeEventListener("change", onChange)
  }, [])
  //Retorna true se for mobile, false caso contrário.
  return !!isMobile
}
