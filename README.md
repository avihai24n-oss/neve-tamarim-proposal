# נווה תמרים — הצעת מחיר לסרטון AI

פרויקט עצמאי לבניית **דף נחיתה / הצעת מחיר** לסרטון בינה מלאכותית ללקוח גדול.
כל המפתחות, ה-wrappers של fal.ai והנכסים של מותג TodoAI מיובאים לכאן, מוכנים לעבודה.

## מבנה

```
.env                       FAL_KEY + BYTEPLUS_KEY (לא נכנס ל-git)
lib/
  fal.py                   יצירת תמונות (gpt-image-2, nano-banana-2) — wrapper מלא
  fal_video.py             יצירת וידאו (kling, seedance, veo3) + lipsync
scripts/
  gen_image.py             CLI ליצירת תמונה → assets/
  gen_video.py             CLI ליצירת וידאו → assets/
references/
  ai-creative-prompting.md מדריך פרומפטינג ל-AI creative
  todoai-brand-guide.md    שפת המותג של TodoAI (צבעים, פונט, לוגו, חתימה)
  todoai-proposal-template.html  תבנית הצעת מחיר מוכנה של TodoAI
assets/                    תמונות/וידאו שנוצרו (לא נכנס ל-git)
proposals/                 קובצי ה-HTML הסופיים של הצעת המחיר
```

## הרצה מהירה

```bash
pip install -r requirements.txt          # requests, playwright, Pillow

# תמונה להירו
python scripts/gen_image.py "..." --model gpt-image-2 --aspect 16:9 --out assets/hero.png

# וידאו (טקסט→וידאו או הנפשת סטיל)
python scripts/gen_video.py "..." --model kling --aspect 16:9 --out assets/hero.mp4
python scripts/gen_video.py "..." --image assets/hero.png --model seedance
```

## מותג TodoAI (מ-references/todoai-brand-guide.md)

- רקע קרם `#F4F4F2`, מסמך לבן, פונט **Heebo**, אקסנט **קורל `#F2542D`**
- לוגו: `https://avihai24n-oss.github.io/webinar/assets/todoai-icon.png`
- חתימה: אביחי אלנקווה · Co-Founder & AI Lead, TodoAI Studio
- בלי em-dash (—) אף פעם · פינות חדות (radius 4px) · RTL
- קישורים: app.todowith.ai · todowith.ai · wa.me/972542064301 · instagram.com/todoai.il

## מודלים זמינים ב-fal.ai

| סוג | מודל | שימוש |
|-----|------|-------|
| תמונה | `gpt-image-2` | איכות גבוהה, טקסט בתמונה |
| תמונה | `nano-banana-2` | Gemini 3.1 Flash, image-to-image, עד 4K |
| וידאו | `kling` v2.5 turbo pro | תנועה + היצמדות לפרומפט |
| וידאו | `seedance` v1 pro | קולנועי, מהיר |
| וידאו | `veo3` | אודיו + דיאלוג, פרימיום |
| lipsync | `infinitalk` | פורטרט + אודיו → דמות מדברת |
