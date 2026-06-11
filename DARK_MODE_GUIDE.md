# 🌙 Dark Mode / Light Mode Toggle Guide

## ✨ Features Implemented

### 1. Theme Toggle Button
- Located in the top-right corner of the header
- Shows 🌙 icon for switching to Dark Mode
- Shows ☀️ icon for switching to Light Mode
- Smooth hover effects and animations

### 2. Color Palettes

#### 🌙 Dark Mode
```css
Background: #1a1a2e (Deep blue-black)
Cards: #16213e (Navy blue)
Text: #eaeaea (Light gray)
Secondary Text: #a0a0a0 (Medium gray)
User Messages: Purple gradient (same as light mode)
Bot Messages: #2d3748 (Dark gray)
Borders: #3a3a52 (Subtle gray)
Hover: #252541 (Slightly lighter)
```

#### ☀️ Light Mode
```css
Background: #f8f9fa (Light gray)
Cards: #ffffff (White)
Text: #212529 (Dark gray)
Secondary Text: #6c757d (Medium gray)
User Messages: Purple gradient
Bot Messages: #f1f3f5 (Light gray)
Borders: #e9ecef (Light border)
Hover: #f8f9ff (Light purple tint)
```

### 3. Smooth Transitions
- All color changes animate smoothly with `transition: all 0.3s ease`
- Applies to:
  - Background colors
  - Text colors
  - Card backgrounds
  - Message bubbles
  - Borders
  - Shadows

### 4. Components Affected
✅ Main background
✅ Header (gradient stays same, looks good on both)
✅ Sidebar
✅ Chat messages (user & bot)
✅ History cards
✅ Buttons
✅ Input fields
✅ Info boxes
✅ Metrics
✅ Timestamps
✅ All text elements

## 🚀 How to Use

1. **Start the app:**
   ```bash
   python -m streamlit run app_history.py
   ```

2. **Toggle theme:**
   - Click the button in the top-right corner
   - Button shows current mode you can switch TO
   - 🌙 = Click to enable Dark Mode
   - ☀️ = Click to enable Light Mode

3. **Theme persists:**
   - Your theme choice is saved in session state
   - Stays active during your entire session
   - Resets to Light Mode on app restart

## 🎨 Design Philosophy

### Dark Mode Benefits
- Reduces eye strain in low-light environments
- Modern, professional appearance
- Better for OLED screens (saves battery)
- Popular among developers

### Light Mode Benefits
- Better readability in bright environments
- Traditional, familiar interface
- Higher contrast for some users
- Better for printing/screenshots

## 🔧 Technical Implementation

### Session State
```python
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False
```

### Dynamic CSS Function
```python
def get_theme_css(dark_mode):
    if dark_mode:
        return """<style>/* Dark mode CSS */</style>"""
    else:
        return """<style>/* Light mode CSS */</style>"""
```

### Toggle Button
```python
theme_icon = "🌙" if not st.session_state.dark_mode else "☀️"
theme_label = "Dark" if not st.session_state.dark_mode else "Light"

if st.button(f"{theme_icon} {theme_label}"):
    st.session_state.dark_mode = not st.session_state.dark_mode
    st.rerun()
```

## 📱 Responsive Design

Both themes work perfectly on:
- Desktop browsers
- Tablets
- Mobile devices
- Different screen sizes

## 🎯 Best Practices

1. **Contrast Ratios:** Both themes maintain WCAG AA contrast standards
2. **Consistency:** All UI elements follow the same color scheme
3. **Accessibility:** Text remains readable in both modes
4. **Performance:** Theme switching is instant with smooth transitions
5. **User Choice:** Respects user preference for their environment

## 🐛 Troubleshooting

**Theme not switching?**
- Make sure you're clicking the toggle button
- Check browser console for errors
- Try refreshing the page

**Colors look wrong?**
- Clear browser cache
- Check if custom CSS is being applied
- Verify session state is working

**Transitions not smooth?**
- Check if browser supports CSS transitions
- Verify transition CSS is not being overridden

## 🎉 Enjoy Your New Theme Toggle!

The chatbot now adapts to your preferred viewing environment. Whether you're coding late at night or working in a bright office, you have the perfect theme for your needs!
