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
  margin: 1rem 0 1.25rem;
  padding: 1rem 1.05rem;
  border: 1px solid var(--lightgray);
  border-radius: 18px;
  background: color-mix(in srgb, var(--light) 94%, transparent);
  display: grid;
  gap: 0.85rem;
}

.hermes-trigger-card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 0.8rem;
}

.hermes-trigger-card-header h2 {
  margin: 0.15rem 0 0;
  font-size: 1rem;
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
}

.hermes-trigger-body,
.hermes-trigger-feedback,
.hermes-trigger-details {
  margin: 0;
}

.hermes-trigger-output {
  display: grid;
  gap: 0.45rem;
}

.hermes-trigger-output-label {
  margin: 0;
  font-size: 0.86rem;
  color: var(--gray);
}

.hermes-trigger-output-textarea {
  width: 100%;
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

@media (max-width: 700px) {
  .hermes-trigger-card {
    padding: 0.9rem;
  }

  .hermes-trigger-card-header {
    flex-direction: column;
  }

  .hermes-trigger-actions {
    display: grid;
  }

  .hermes-trigger-button {
    width: 100%;
  }
}
`

HermesTrigger.afterDOMLoaded = script

export default (() => HermesTrigger) satisfies QuartzComponentConstructor
