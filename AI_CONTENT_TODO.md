# AI Content Generation TODO
**Project:** Unmuted - School Project
**Goal:** Fully flesh out the site with AI-generated content

---

## 🎨 Phase 1: Visual Content (HIGH PRIORITY)

### Video Thumbnails for Playlists Page
- [ ] **36 AI-generated video thumbnails** (6 per show)
  - Gossip Girl (6 thumbnails)
  - Pretty Little Liars (6 thumbnails)
  - Teen Wolf (6 thumbnails)
  - The Vampire Diaries (6 thumbnails)
  - Glee (6 thumbnails)
  - The O.C. (6 thumbnails)
- **Style:** Teen drama screenshot aesthetic with text overlays
- **Tool:** Midjourney, DALL-E, or Canva
- **Location:** `/static/images/videos/[show-name]/`

### Creator Avatars
- [ ] **5 AI-generated creator profile pictures**
  - maria (Latina, 20s)
  - jay (non-binary, Asian, 20s)
  - keisha (Black woman, 20s)
  - alex (white woman, 20s)
  - sam (Middle Eastern man, 20s)
- **Style:** Diverse, Gen Z, casual
- **Tool:** Midjourney, DALL-E
- **Location:** `/static/images/creators/`

---

## 📝 Phase 2: Text Content (MEDIUM PRIORITY)

### Creator Bios & Profiles
- [ ] Create "Creators" page (`/content/pages/creators.md`)
- [ ] Write bio for each creator (150-200 words each)
  - Background
  - Why they love teen dramas
  - Their unique perspective
  - Favorite show
- [ ] Add social media handles (fake but realistic)

### Video Descriptions
- [ ] Expand video metadata in playlists.md
  - Add 2-3 sentence description per video
  - Add tags/topics covered
  - Add "Key Moments" timestamps

---

## 🎬 Phase 3: Interactive Elements (LOW PRIORITY)

### Video Player Mockups
- [ ] Create video player UI component
  - Play button overlay
  - Progress bar
  - Duration display
  - Volume controls
- [ ] Make thumbnails "clickable" (opens modal with player mockup)
- [ ] Add "Watch on TikTok" link in modal

### Enhanced Playlists Page
- [ ] Add filter by creator
- [ ] Add sort by (newest, most viewed, etc.)
- [ ] Add "Up Next" queue preview
- [ ] Add playlist stats (total watch time, video count)

---

## 🎯 Phase 4: Polish (OPTIONAL)

### About/Story Page
- [ ] Create "About Unmuted" page
- [ ] Origin story (how it started)
- [ ] Mission statement
- [ ] Team section with creator cards

### Blog/Updates Section
- [ ] Create 3-5 fake blog posts
  - "Why We Started Unmuted"
  - "Breaking Down Representation in Teen Wolf"
  - "The Bonnie Bennett Problem: A Deep Dive"
  - "How We Choose What to Cover"

### Community Features
- [ ] Mock Discord screenshots
- [ ] Fake poll results
- [ ] User submission examples

---

## 📊 AI Generation Prompts (Ready to Use)

### Video Thumbnail Prompt Template:
```
Create a video thumbnail in the style of a teen drama screenshot. 
Show: [Show Name]
Scene: [Description]
Style: Cinematic, 16:9 aspect ratio, slight film grain
Text overlay: "[Video Title]" in bold sans-serif font
Colors: Match the show's aesthetic (dark/moody for TVD, bright/preppy for Gossip Girl, etc.)
```

### Creator Avatar Prompt Template:
```
Portrait photo of a [age] year old [ethnicity] [gender] content creator.
Style: Casual, Gen Z aesthetic, natural lighting
Setting: Simple background, focus on face
Mood: Friendly, approachable, confident
Camera: Eye-level, slight smile
Clothing: Casual (hoodie, t-shirt, etc.)
```

---

## 📁 File Structure to Create

```
/static/images/
  /videos/
    /gossip-girl/
      - video-1.jpg
      - video-2.jpg
      ...
    /pretty-little-liars/
    /teen-wolf/
    /vampire-diaries/
    /glee/
    /the-oc/
  /creators/
    - maria.jpg
    - jay.jpg
    - keisha.jpg
    - alex.jpg
    - sam.jpg
  /mockups/
    - video-player.png
    - discord-screenshot.png

/content/pages/
  - creators.md (NEW)
  - about.md (NEW)
```

---

## 🚀 Quick Wins (Start Here)

1. **Generate 5 creator avatars** - Makes testimonials and video credits feel real
2. **Create 6 video thumbnails for Gossip Girl** - Proves the concept works
3. **Write creator bios** - Adds depth to the "multiple voices" claim
4. **Add video player mockup** - Makes playlists page interactive

---

## Notes

- Keep all AI-generated content in `/static/images/` for easy management
- Use consistent naming: `[show-name]-[number].jpg` for videos
- Save AI prompts used so you can regenerate if needed
- Consider adding watermark: "Concept Design - School Project" on some assets

---

**Last Updated:** October 9, 2025
**Status:** Planning Phase
