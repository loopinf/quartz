import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./types"
import { classNames } from "../util/lang"
// @ts-ignore
import script from "./scripts/hermes-trigger.inline"

const HermesTrigger: QuartzComponent = ({ fileData, displayClass }: QuartzComponentProps) => {
  const frontmatter = (fileData.frontmatter ?? {}) as Record<string, unknown>
  const pageName = String(frontmatter.name ?? frontmatter.title ?? fileData.slug ?? "")
  const entityType = String(frontmatter.entity_type ?? "")
  const themeTags = Array.isArray(frontmatter.theme_tags)
    ? frontmatter.theme_tags.join(", ")
    : String(frontmatter.theme_tags ?? "")
  const sourceNote = String(frontmatter.source_note ?? "")
  const updatedAt = String(frontmatter.updated_at ?? frontmatter.modified ?? "")
  const slug = String(fileData.slug ?? "")
  const entityName = String(frontmatter.name ?? frontmatter.title ?? "")

  if (!pageName || !slug) {
    return null
  }

  return (
    <section
      class={classNames(displayClass, "hermes-trigger-card")}
      data-hermes-trigger-card="1"
      data-page-name={pageName}
      data-page-slug={slug}
      data-entity-type={entityType}
      data-theme-tags={themeTags}
      data-source-note={sourceNote}
      data-updated-at={updatedAt}
      data-entity-name={entityName}
    >
      <div class="hermes-trigger-card-header">
        <div>
          <p class="hermes-trigger-eyebrow">Hermes discussion trigger</p>
          <h2>이 페이지 기준 질문 초안 만들기</h2>
        </div>
        <span class="hermes-trigger-badge">step 1</span>
      </div>

      <p class="hermes-trigger-body">
        이 버튼은 Hermes를 직접 호출하지 않습니다. 현재 페이지 맥락을 넣은 템플릿을 복사해서
        Discord에 붙여 넣는 용도입니다.
      </p>

      <div class="hermes-trigger-actions">
        <button
          type="button"
          class="hermes-trigger-button hermes-trigger-button-primary"
          data-hermes-template="general"
        >
          Hermes 질문 시작
        </button>
        <button type="button" class="hermes-trigger-button" data-hermes-template="relationship">
          관계 질문 템플릿 복사
        </button>
      </div>

      <p class="hermes-trigger-feedback" aria-live="polite"></p>

      <div class="hermes-trigger-output" hidden>
        <p class="hermes-trigger-output-label">
          복사 실패 시 아래 내용을 직접 복사해서 붙여 넣으면 됩니다.
        </p>
        <textarea class="hermes-trigger-output-textarea" readonly rows={14}></textarea>
      </div>

      <div class="hermes-trigger-stage2" data-hermes-stage2>
        <div class="hermes-trigger-card-header">
          <div>
            <p class="hermes-trigger-eyebrow">Hermes 토론 요청</p>
            <h2>이 페이지로 새 Discord 스레드 만들기</h2>
          </div>
          <span class="hermes-trigger-badge hermes-trigger-badge-stage2">step 2</span>
        </div>
        <p class="hermes-trigger-body">
          현재 페이지 컨텍스트와 입력한 질문으로 <strong>새 Discord 토론 스레드</strong>를 즉시
          생성합니다. 기존 채널/스레드에는 글이 올라가지 않고, 항상 이 요청 전용 스레드가 새로
          만들어집니다. 동시에 <code>content/market-intel/hermes-inbox/</code>에 감사용 마크다운이
          저장됩니다. 로컬 헬퍼(<code>scripts/hermes_inbox_server.py</code>)가 켜져 있어야 합니다.
        </p>
        <textarea
          class="hermes-trigger-stage2-textarea"
          rows={5}
          placeholder="여기에 질문/의견을 적어주세요. 페이지 컨텍스트는 자동으로 붙습니다."
          data-hermes-stage2-input
        ></textarea>
        <div class="hermes-trigger-actions">
          <button
            type="button"
            class="hermes-trigger-button hermes-trigger-button-primary"
            data-hermes-stage2-submit
          >
            새 Discord 스레드 만들기
          </button>
        </div>
        <p class="hermes-trigger-feedback" data-hermes-stage2-feedback aria-live="polite"></p>
      </div>

      <details class="hermes-trigger-details">
        <summary>무슨 템플릿이 복사되는지 보기</summary>
        <ul>
          <li>
            <strong>Hermes 질문 시작</strong>: 현재 종목/페이지 기준으로 핵심 포인트, 연결 테마,
            리스크, 다음 문서를 물어보는 기본 템플릿
          </li>
          <li>
            <strong>관계 질문 템플릿 복사</strong>: 현재 종목과 다른 종목/이벤트의 직접·간접 관계를
            정리해 달라고 요청하는 템플릿
          </li>
        </ul>
      </details>
    </section>
  )
}

HermesTrigger.css = `
.hermes-trigger-card {
  margin: 1.5rem 0 0;
  padding: 1rem 1.05rem;
  border: 1px solid var(--lightgray);
  border-radius: 18px;
  background: color-mix(in srgb, var(--light) 94%, transparent);
  display: grid;
  gap: 0.85rem;
  box-sizing: border-box;
  width: 100%;
  max-width: 100%;
  overflow-x: clip;
}

.hermes-trigger-card *,
.hermes-trigger-card *::before,
.hermes-trigger-card *::after {
  box-sizing: border-box;
}

.hermes-trigger-card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 0.8rem;
  min-width: 0;
}

.hermes-trigger-card-header > div {
  min-width: 0;
}

.hermes-trigger-card-header h2 {
  margin: 0.15rem 0 0;
  font-size: 1rem;
  overflow-wrap: anywhere;
}

.hermes-trigger-eyebrow {
  margin: 0;
  color: var(--secondary);
  font-size: 0.72rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

.hermes-trigger-badge {
  display: inline-flex;
  align-items: center;
  border-radius: 999px;
  padding: 0.24rem 0.55rem;
  background: color-mix(in srgb, #7b8cff 18%, var(--light) 82%);
  color: var(--dark);
  font-size: 0.75rem;
  font-weight: 700;
  white-space: nowrap;
  flex-shrink: 0;
}

.hermes-trigger-body,
.hermes-trigger-feedback,
.hermes-trigger-details {
  margin: 0;
}

.hermes-trigger-body,
.hermes-trigger-feedback,
.hermes-trigger-output-label,
.hermes-trigger-details,
.hermes-trigger-card code,
.hermes-trigger-card a,
.hermes-trigger-card summary,
.hermes-trigger-card li {
  overflow-wrap: anywhere;
  word-break: break-word;
}

.hermes-trigger-output {
  display: grid;
  gap: 0.45rem;
  min-width: 0;
}

.hermes-trigger-output-label {
  margin: 0;
  font-size: 0.86rem;
  color: var(--gray);
}

.hermes-trigger-output-textarea {
  width: 100%;
  max-width: 100%;
  min-height: 13rem;
  resize: vertical;
  border-radius: 12px;
  border: 1px solid var(--lightgray);
  background: color-mix(in srgb, var(--light) 97%, transparent);
  color: var(--dark);
  font: 0.88rem/1.45 var(--bodyFont);
  padding: 0.8rem;
}

.hermes-trigger-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 0.6rem;
  min-width: 0;
}

.hermes-trigger-button {
  border: 1px solid var(--lightgray);
  background: transparent;
  color: var(--secondary);
  border-radius: 12px;
  padding: 0.7rem 0.95rem;
  font: inherit;
  font-weight: 700;
  cursor: pointer;
  max-width: 100%;
}

.hermes-trigger-button:hover {
  border-color: var(--secondary);
}

.hermes-trigger-button-primary {
  background: #24304f;
  color: #f5f7ff;
  border-color: #24304f;
}

.hermes-trigger-feedback {
  min-height: 1.1rem;
  color: var(--gray);
  font-size: 0.86rem;
}

.hermes-trigger-feedback.is-success {
  color: #2b8a3e;
}

.hermes-trigger-feedback.is-error {
  color: #b54708;
}

.hermes-trigger-details {
  font-size: 0.92rem;
}

.hermes-trigger-details summary {
  cursor: pointer;
  color: var(--secondary);
  font-weight: 600;
}

.hermes-trigger-details ul {
  margin: 0.55rem 0 0 1.1rem;
}

.hermes-trigger-stage2 {
  display: grid;
  gap: 0.6rem;
  padding-top: 0.85rem;
  border-top: 1px dashed var(--lightgray);
  min-width: 0;
}

.hermes-trigger-stage2-textarea {
  width: 100%;
  max-width: 100%;
  resize: vertical;
  border-radius: 12px;
  border: 1px solid var(--lightgray);
  background: color-mix(in srgb, var(--light) 97%, transparent);
  color: var(--dark);
  font: 0.92rem/1.45 var(--bodyFont);
  padding: 0.7rem;
}

.hermes-trigger-badge-stage2 {
  background: color-mix(in srgb, #2b8a3e 22%, var(--light) 78%);
}

@media (max-width: 700px) {
  .hermes-trigger-card {
    padding: 0.9rem;
    margin-top: 1.25rem;
  }

  .hermes-trigger-card-header {
    flex-direction: column;
  }

  .hermes-trigger-badge {
    align-self: flex-start;
  }

  .hermes-trigger-actions {
    display: grid;
    grid-template-columns: minmax(0, 1fr);
  }

  .hermes-trigger-button {
    width: 100%;
  }

  .hermes-trigger-output-textarea,
  .hermes-trigger-stage2-textarea {
    font-size: 16px;
  }
}
`

HermesTrigger.afterDOMLoaded = script

export default (() => HermesTrigger) satisfies QuartzComponentConstructor
