import * as React from "react"

import type {
  ToastActionElement,
  ToastProps,
} from "@/components/ui/toast"

// Limite máximo de toasts que podem aparecer simultaneamente na tela
const TOAST_LIMIT = 1
// Tempo em milissegundos que o toast permanece antes de ser removido após o dismiss
const TOAST_REMOVE_DELAY = 1000000

// Tipo que representa um toast completo, com id único e conteúdo opcional (título, descrição, ação)
type ToasterToast = ToastProps & {
  id: string
  title?: React.ReactNode
  description?: React.ReactNode
  action?: ToastActionElement
}

// Defino os tipos de ações que o reducer vai receber para manipular os toasts
const actionTypes = {
  ADD_TOAST: "ADD_TOAST",
  UPDATE_TOAST: "UPDATE_TOAST",
  DISMISS_TOAST: "DISMISS_TOAST",
  REMOVE_TOAST: "REMOVE_TOAST",
} as const

// Contador simples para gerar ids únicos para cada toast criado
let count = 0
function genId() {
  count = (count + 1) % Number.MAX_SAFE_INTEGER
  return count.toString()
}

type ActionType = typeof actionTypes

// Definição das possíveis ações que podem ser disparadas e seus dados
type Action =
  | {
      type: ActionType["ADD_TOAST"]
      toast: ToasterToast
    }
  | {
      type: ActionType["UPDATE_TOAST"]
      toast: Partial<ToasterToast>
    }
  | {
      type: ActionType["DISMISS_TOAST"]
      toastId?: ToasterToast["id"]
    }
  | {
      type: ActionType["REMOVE_TOAST"]
      toastId?: ToasterToast["id"]
    }

// Estado do sistema de toasts: um array com os toasts ativos
interface State {
  toasts: ToasterToast[]
}

// Mapa para armazenar timeouts pendentes de remoção de toasts, para evitar múltiplos timers para o mesmo toast
const toastTimeouts = new Map<string, ReturnType<typeof setTimeout>>()

// Função que agenda a remoção do toast após o delay configurado, garantindo que não haja timers duplicados
const addToRemoveQueue = (toastId: string) => {
  if (toastTimeouts.has(toastId)) {
    return
  }

  const timeout = setTimeout(() => {
    toastTimeouts.delete(toastId)
    dispatch({
      type: "REMOVE_TOAST",
      toastId: toastId,
    })
  }, TOAST_REMOVE_DELAY)

  toastTimeouts.set(toastId, timeout)
}

// Reducer que trata as ações enviadas para manipular o estado dos toasts
export const reducer = (state: State, action: Action): State => {
  switch (action.type) {
    case "ADD_TOAST":
      // Adiciona o toast no topo da lista e respeita o limite máximo configurado
      return {
        ...state,
        toasts: [action.toast, ...state.toasts].slice(0, TOAST_LIMIT),
      }

    case "UPDATE_TOAST":
      // Atualiza o toast correspondente com os novos dados recebidos
      return {
        ...state,
        toasts: state.toasts.map((t) =>
          t.id === action.toast.id ? { ...t, ...action.toast } : t
        ),
      }

    case "DISMISS_TOAST": {
      const { toastId } = action

      // Quando um toast é dispensado, agenda sua remoção futura pelo timeout
      if (toastId) {
        addToRemoveQueue(toastId)
      } else {
        // Se nenhum id específico, agenda a remoção de todos
        state.toasts.forEach((toast) => {
          addToRemoveQueue(toast.id)
        })
      }

      // Marca o toast (ou todos) como fechados para atualizar a UI imediatamente
      return {
        ...state,
        toasts: state.toasts.map((t) =>
          t.id === toastId || toastId === undefined
            ? {
                ...t,
                open: false,
              }
            : t
        ),
      }
    }

    case "REMOVE_TOAST":
      // Remove imediatamente o toast do estado após o timeout
      if (action.toastId === undefined) {
        return {
          ...state,
          toasts: [],
        }
      }
      return {
        ...state,
        toasts: state.toasts.filter((t) => t.id !== action.toastId),
      }
  }
}

// Lista de funções que vão ser notificadas sempre que o estado dos toasts mudar (padrão observer)
const listeners: Array<(state: State) => void> = []

// Estado na memória, único e compartilhado, para gerenciar os toasts globalmente
let memoryState: State = { toasts: [] }

// Função para disparar ações que atualizam o estado e notificam os listeners
function dispatch(action: Action) {
  memoryState = reducer(memoryState, action)
  listeners.forEach((listener) => {
    listener(memoryState)
  })
}

// Tipo de toast para ser passado na função toast, sem o id que será gerado automaticamente
type Toast = Omit<ToasterToast, "id">

// Função principal para criar um novo toast, adicioná-lo e retornar métodos para atualizar e dispensar ele
function toast({ ...props }: Toast) {
  const id = genId()

  const update = (props: ToasterToast) =>
    dispatch({
      type: "UPDATE_TOAST",
      toast: { ...props, id },
    })
  const dismiss = () => dispatch({ type: "DISMISS_TOAST", toastId: id })

  dispatch({
    type: "ADD_TOAST",
    toast: {
      ...props,
      id,
      open: true,
      onOpenChange: (open) => {
        if (!open) dismiss()
      },
    },
  })

  return {
    id: id,
    dismiss,
    update,
  }
}

// Hook React para consumir o estado dos toasts em componentes funcionais React
function useToast() {
  // Estado local que espelha o estado global em memória
  const [state, setState] = React.useState<State>(memoryState)

  React.useEffect(() => {
    // Adiciona o setState na lista de listeners para receber atualizações
    listeners.push(setState)
    // Remove o listener ao desmontar para evitar vazamentos
    return () => {
      const index = listeners.indexOf(setState)
      if (index > -1) {
        listeners.splice(index, 1)
      }
    }
  }, [state])

  // Retorna o estado e funções para manipular toasts na UI
  return {
    ...state,
    toast,
    dismiss: (toastId?: string) => dispatch({ type: "DISMISS_TOAST", toastId }),
  }
}

export { useToast, toast }