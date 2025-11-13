import streamlit as st
import streamlit.components.v1 as components

def show_install_prompt():
    """Show PWA install prompt for mobile users"""

    components.html("""
    <script>
    let deferredPrompt;

    window.addEventListener('beforeinstallprompt', (e) => {
      e.preventDefault();
      deferredPrompt = e;

      // Show install banner
      const banner = document.createElement('div');
      banner.innerHTML = `
        <div style="
          position: fixed;
          bottom: 0;
          left: 0;
          right: 0;
          background: linear-gradient(135deg, #E91E63, #F06292);
          color: white;
          padding: 1rem;
          text-align: center;
          box-shadow: 0 -4px 20px rgba(0,0,0,0.3);
          z-index: 10000;
          animation: slideUp 0.5s ease-out;
        ">
          <div style="font-size: 1.1rem; font-weight: bold; margin-bottom: 0.5rem;">
            📱 Install Breast Friend Forever
          </div>
          <div style="font-size: 0.9rem; margin-bottom: 1rem;">
            Get the app on your phone for quick access!
          </div>
          <button onclick="installApp()" style="
            background: white;
            color: #E91E63;
            border: none;
            padding: 0.8rem 2rem;
            border-radius: 25px;
            font-size: 1rem;
            font-weight: bold;
            cursor: pointer;
            margin-right: 1rem;
          ">
            Install Now
          </button>
          <button onclick="dismissBanner()" style="
            background: transparent;
            color: white;
            border: 2px solid white;
            padding: 0.8rem 2rem;
            border-radius: 25px;
            font-size: 1rem;
            cursor: pointer;
          ">
            Maybe Later
          </button>
        </div>
      `;

      banner.id = 'installBanner';
      document.body.appendChild(banner);
    });

    window.installApp = async () => {
      if (deferredPrompt) {
        deferredPrompt.prompt();
        const { outcome } = await deferredPrompt.userChoice;
        console.log(`User response: ${outcome}`);
        deferredPrompt = null;
        dismissBanner();
      }
    };

    window.dismissBanner = () => {
      const banner = document.getElementById('installBanner');
      if (banner) {
        banner.style.animation = 'slideDown 0.5s ease-out';
        setTimeout(() => banner.remove(), 500);
      }
    };
    </script>

    <style>
    @keyframes slideUp {
      from { transform: translateY(100%); }
      to { transform: translateY(0); }
    }
    @keyframes slideDown {
      from { transform: translateY(0); }
      to { transform: translateY(100%); }
    }
    </style>
    """, height=0)
