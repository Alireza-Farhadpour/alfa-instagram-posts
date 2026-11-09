# Runbook: nightly alfa.pmi Instagram carousel (approval mode)

This repo hosts the public slide images for the alfa.pmi Instagram page and the kit to build them.
A scheduled run gets one topic (and optional points) and follows these steps. The user is an
experienced project planning & control trainer (PMBOK 8, Primavera P6, MS Project, agile).

## 0. Setup
1. Attach this repo with push access (add_repo owner=Alireza-Farhadpour repo=alfa-instagram-posts access=push), clone it.
2. Work dir: `mkdir -p ~/post && cp -r kit/assets ~/post/assets && cp kit/template/ccm_post_template.py ~/post/build.py`
3. `cd ~/post && npm init -y && npm i @fontsource/vazirmatn @fontsource/source-sans-3 lucide-static`
4. Render with Playwright + `/usr/bin/google-chrome` (as in the template). Install playwright with pip if missing.
5. If the claude.ai project "Project Management Agent" is available (Projects tool), use project_search on the
   PMBOK 8 Guide and the user's course notes (files "2.x#PMBOK 8th Guide-…-Col.pdf") to anchor the content.

## 1. Content (Persian, for managers/planners/PMO staff)
- 7–9 slides: cover → what/why → 3–4 core slides (one idea each, a chart/diagram as the hero) → practical example
  or how-to → engagement slide (question with numbered options, "شماره‌اش را کامنت کنید", save/send, @alfa.pmi | www.alfapmi.com).
- ≤ ~30 words per slide. English term in parentheses on first use. Accurate: never attribute to PMBOK 8 what it
  does not say; for product facts (P6, MS Project) verify with a web search first. No invented statistics.
- Paraphrase PMBOK; never copy passages.

## 2. Design (approved style; copy the structure of kit/template/ccm_post_template.py, see kit/examples/)
- Cover rule (MANDATORY): Persian title box; the English box sits on the bottom line of the Persian box, shorter, centred.
  Big orange-gold number or keyword, keyword in glowing cyan, chevrons on top, orange arc, a NEW topic illustration
  drawn in SVG in the middle, small horizontal logo at the bottom, small PMBOK 8 stamp bottom-right (only if the topic
  is PMBOK-based).
- Palette: navy bg (assets/content_bg.png), gold #AE9471, cyan #00B0F0, orange #FF9A3C, red #FF3D5A, lavender #B4C7E7.
- Sizes: titles 58px, body 36–39px, card titles 46px, English subtitles 44px. Fonts: Vazirmatn (Persian), Source Sans 3 (English).
- Content slides: chip on top, title + accent line, hero chart panel, short def card, optional cyan answer chip, swipe bar.
- Gotcha: no blur filter on perfectly vertical/horizontal SVG lines (they vanish).
- QA: render, make a contact sheet, LOOK at every slide (overlaps, clipped text, RTL/LTR mix-ups, label collisions). Fix and re-render.

## 3. Caption
Hook question on line 1 → short body naming the key points → "…؟ در کامنت بنویسید 💬" → "ذخیره کنید … 📌" →
course/website line ("سایت: www.alfapmi.com") → exactly 5 hashtags (Instagram allows max 5): #مدیریت_پروژه,
#برنامه_ریزی_و_کنترل_پروژه, one topic hashtag, one more relevant hashtag (e.g. #PMBOK8), #alfapmi. ≤ 2,200 characters.

## 4. Upload images
Convert slides to JPEG (quality 90, 1080x1080). Commit to `posts/<YYYY-MM-DD>/01.jpg … NN.jpg` plus `caption.txt`, push to main.
Public URL: `https://raw.githubusercontent.com/Alireza-Farhadpour/alfa-instagram-posts/main/posts/<date>/NN.jpg`
(check each URL returns 200 image/jpeg).

## 5. Ask for approval (do NOT publish before the user approves)
- Send the slides (SendUserFile) and the caption (SendUserMessage) and a PushNotification:
  "پست امشب آماده است؛ برای انتشار ساعت ۱۹ تأیید کنید."
- Messages to the user are in Persian, plain text, each paragraph starting with a Persian word and an RLM (U+200F).
- If the user asks for changes: apply them, re-render, re-push, re-send.
- When the user approves: if it is before 19:00 Tehran, schedule a wake-up in this session with send_later at
  19:00 [Asia/Tehran] ("publish the approved post"); if it is already past 19:00, publish now.
- If there is no approval, publish nothing.

## 6. Publish (Composio, Instagram account alias "alfa.pmi", ig_user_id 39892526913695793)
1. INSTAGRAM_CREATE_CAROUSEL_CONTAINER with child_image_urls (ordered raw URLs, 2–10) and the caption.
2. INSTAGRAM_POST_IG_USER_MEDIA_PUBLISH with the returned creation_id (parent id, not child ids).
3. INSTAGRAM_GET_IG_MEDIA for the permalink; send the link to the user. On failure, report the exact error; do not retry blindly more than once.
