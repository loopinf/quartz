function fallbackCopy(text: string) {
  const textarea = document.createElement("textarea")
  textarea.value = text
  textarea.setAttribute("readonly", "true")
  textarea.style.position = "fixed"
  textarea.style.opacity = "0"
  document.body.appendChild(textarea)
  textarea.select()
  document.execCommand("copy")
  document.body.removeChild(textarea)
}

function buildPrompt(card: HTMLElement, template: string) {
  const pageName = card.dataset.pageName ?? ""
  const pageSlug = card.dataset.pageSlug ?? ""
  const entityType = card.dataset.entityType ?? ""
  const themeTags = card.dataset.themeTags ?? ""
  const sourceNote = card.dataset.sourceNote ?? ""
  const updatedAt = card.dataset.updatedAt ?? ""
  const currentUrl = window.location.href

  const header = [
    "[Hermes market-intel page context]",
    `- page_name: ${pageName}`,
    `- page_slug: ${pageSlug}`,
    `- page_url: ${currentUrl}`,
    `- entity_type: ${entityType || "unknown"}`,
    `- theme_tags: ${themeTags || ""}`,
    `- source_note: ${sourceNote || ""}`,
    `- updated_at: ${updatedAt || ""}`,
    "",
  ]

  if (template === "relationship") {
    return header
      .concat([
        "[Question]",
        `${pageName}와 [비교/관계 대상]의 관계를 정리해줘.`,
        "",
        "아래 형식으로 답변:",
        "1. 직접 관계 여부 (공급망, 고객/벤더, 지분, 프로젝트, 경쟁)",
        "2. 간접 관계 여부 (같은 테마, 원자재/가격 연동, 정책/수급 연결)",
        "3. market-intel 기준으로 더 확인해야 할 이벤트/엔티티/문서",
        "4. 페이지로 승격할 만한 정리라면 어떤 note 구조가 좋은지",
        "",
        "내 가설:",
        "- ",
        "",
        "특히 궁금한 점:",
        "- ",
      ])
      .join("\n")
  }

  return header
    .concat([
      "[Question]",
      `현재 페이지(${pageName}) 기준으로 아래 형식으로 정리해줘.`,
      "",
      "1. 핵심 포인트 3개",
      "2. 지금 연결되는 테마/이벤트",
      "3. 가장 먼저 확인할 리스크/반론",
      "4. market-intel 내부에서 다음에 볼 문서/페이지",
      "",
      "내 의견:",
      "- ",
      "",
      "추가 질문:",
      "- ",
    ])
    .join("\n")
}

const HERMES_INBOX_ENDPOINT = "http://127.0.0.1:8765/api/hermes-request"

async function submitStage2Request(card: HTMLElement, text: string) {
  const payload = {
    source_page_title: card.dataset.pageName ?? "",
    source_page_path: card.dataset.pageSlug ?? "",
    source_page_url: window.location.href,
    entity_type: card.dataset.entityType ?? "",
    entity_name: card.dataset.entityName ?? card.dataset.pageName ?? "",
    request_text: text,
  }
  const res = await fetch(HERMES_INBOX_ENDPOINT, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  })
  const body = (await res.json().catch(() => ({}))) as Record<string, unknown>
  if (!res.ok || !body.ok) {
    const reason = typeof body.error === "string" ? body.error : `HTTP ${res.status}`
    throw new Error(reason)
  }
  return body as {
    request_id: string
    path: string
    discord_thread_id?: string
    discord_thread_url?: string
    discord_thread_name?: string
  }
}

function bindStage2(card: HTMLElement) {
  const stage2 = card.querySelector("[data-hermes-stage2]") as HTMLElement | null
  if (!stage2) return
  const input = stage2.querySelector("[data-hermes-stage2-input]") as HTMLTextAreaElement | null
  const submit = stage2.querySelector("[data-hermes-stage2-submit]") as HTMLButtonElement | null
  const feedback = stage2.querySelector("[data-hermes-stage2-feedback]") as HTMLElement | null
  if (!input || !submit) return
  if (submit.dataset.hermesBound === "1") return
  submit.dataset.hermesBound = "1"

  const setFeedback = (msg: string, kind: "success" | "error" | "info") => {
    if (!feedback) return
    feedback.textContent = msg
    feedback.classList.remove("is-success", "is-error")
    if (kind === "success") feedback.classList.add("is-success")
    if (kind === "error") feedback.classList.add("is-error")
  }

  const onClick = async () => {
    const text = (input.value ?? "").trim()
    if (!text) {
      setFeedback("질문/의견을 먼저 입력해주세요.", "error")
      input.focus()
      return
    }
    submit.disabled = true
    setFeedback("새 Discord 스레드를 만드는 중…", "info")
    try {
      const result = await submitStage2Request(card, text)
      if (result.discord_thread_url) {
        if (feedback) {
          feedback.classList.remove("is-error")
          feedback.classList.add("is-success")
          feedback.textContent = ""
          const lead = document.createElement("span")
          lead.textContent = "새 Discord 스레드 생성 완료 → "
          const link = document.createElement("a")
          link.href = result.discord_thread_url
          link.target = "_blank"
          link.rel = "noopener noreferrer"
          link.textContent = result.discord_thread_name || result.discord_thread_id || "thread"
          feedback.appendChild(lead)
          feedback.appendChild(link)
          const audit = document.createElement("span")
          audit.textContent = ` (audit: ${result.path})`
          feedback.appendChild(audit)
        }
      } else {
        setFeedback(`요청 처리됨 (audit: ${result.path})`, "success")
      }
      input.value = ""
    } catch (error) {
      const reason = error instanceof Error ? error.message : String(error)
      setFeedback(
        `Discord 스레드 생성 실패 (${reason}). 로컬 헬퍼가 켜져 있고 DISCORD_BOT_TOKEN이 설정되어 있는지 확인해주세요: python3 scripts/hermes_inbox_server.py`,
        "error",
      )
    } finally {
      submit.disabled = false
    }
  }

  submit.addEventListener("click", onClick)
  // @ts-ignore Quartz injects addCleanup on window for SPA navigation cleanup.
  window.addCleanup(() => submit.removeEventListener("click", onClick))
}

document.addEventListener("nav", () => {
  document.querySelectorAll("[data-hermes-trigger-card]").forEach((card) => {
    const element = card as HTMLElement
    const feedback = element.querySelector(
      ".hermes-trigger-feedback:not([data-hermes-stage2-feedback])",
    ) as HTMLElement | null
    const output = element.querySelector(".hermes-trigger-output") as HTMLElement | null
    const textarea = element.querySelector(
      ".hermes-trigger-output-textarea",
    ) as HTMLTextAreaElement | null
    const buttons = element.querySelectorAll("[data-hermes-template]")
    bindStage2(element)

    buttons.forEach((button) => {
      const htmlButton = button as HTMLButtonElement
      if (htmlButton.dataset.hermesBound === "1") {
        return
      }
      htmlButton.dataset.hermesBound = "1"

      const onClick = async () => {
        const template = htmlButton.dataset.hermesTemplate ?? "general"
        const text = buildPrompt(element, template)
        if (textarea) {
          textarea.value = text
        }
        if (output) {
          output.hidden = false
        }
        try {
          if (navigator.clipboard?.writeText) {
            await navigator.clipboard.writeText(text)
          } else {
            fallbackCopy(text)
          }
          if (feedback) {
            feedback.textContent =
              template === "relationship"
                ? "관계 질문 템플릿을 복사했습니다. Discord에 붙여 넣고 비교 대상을 채우면 됩니다."
                : "질문 템플릿을 복사했습니다. Discord에 붙여 넣고 내 의견/추가 질문만 채우면 됩니다."
            feedback.classList.add("is-success")
            feedback.classList.remove("is-error")
          }
        } catch (error) {
          console.error(error)
          if (textarea) {
            textarea.focus()
            textarea.select()
          }
          if (feedback) {
            feedback.textContent =
              "복사에 실패했습니다. 아래 텍스트가 채워졌습니다. 직접 복사해서 Discord에 붙여 넣으면 됩니다."
            feedback.classList.add("is-error")
            feedback.classList.remove("is-success")
          }
        }
      }

      htmlButton.addEventListener("click", onClick)
      // @ts-ignore Quartz injects addCleanup on window for SPA navigation cleanup.
      window.addCleanup(() => htmlButton.removeEventListener("click", onClick))
    })
  })
})
