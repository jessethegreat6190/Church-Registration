import os

html_content = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Admin Panel | Watchmen</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="css/style.css">
</head>
<body>
  <nav>
    <h1>🔍 Watchmen</h1>
    <div class="nav-links">
      <a href="index.html">Gallery</a>
      <a href="upload.html">Upload</a>
      <a href="admin.html" class="active">Admin</a>
      <div id="user-status"></div>
      <button id="auth-toggle" class="btn-primary" onclick="toggleAuth()">Login</button>
    </div>
  </nav>

  <div class="container">
    <div id="admin-restricted" style="display: none;" class="empty-state">
      <div class="auth-container" style="margin: 0 auto;">
        <h2 style="color: #ef4444;">Access Denied</h2>
        <p class="subtitle">Only administrators can access this portal.</p>
        <a href="index.html" class="btn-primary" style="width: 100%; margin-top: 1rem; text-decoration: none;">Return to Gallery</a>
      </div>
    </div>

    <div id="admin-panel-section" style="display: none;">
      <!-- Quick Post Section -->
      <div class="admin-panel">
        <h2 style="margin-bottom: 0.5rem; color: #fff; font-weight: 800;">📤 Quick Post</h2>
        <p style="color: #94a3b8; margin-bottom: 2rem; font-size: 0.9375rem;">Upload directly to the gallery as an administrator</p>
        
        <div class="form-group">
          <label for="admin-image-title">Inspiration Title *</label>
          <input type="text" id="admin-image-title" placeholder="What's this about?">
        </div>
        
        <div class="form-group">
          <label for="admin-image-description">Short Description</label>
          <textarea id="admin-image-description" placeholder="Share the story behind this image..." style="background: #0f172a; border: 1px solid #334155; color: #fff; border-radius: 8px; padding: 0.75rem; width: 100%; min-height: 80px;"></textarea>
        </div>
        
        <div class="form-group">
          <label for="admin-image-file">Image File *</label>
          <input type="file" id="admin-image-file" accept="image/*" style="padding: 0.6rem; background: #0f172a; border: 1px dashed #334155;">
        </div>
        
        <button class="btn-primary" id="admin-upload-btn" onclick="uploadImageAdmin()" style="width: 100%; margin-top: 1rem;">Post to Gallery</button>
        
        <div id="admin-upload-progress" style="display: none; margin-top: 2rem;">
          <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
            <span id="admin-progress-text" style="font-weight: 600; font-size: 0.875rem; color: #cbd5e1;">Uploading...</span>
            <span id="admin-progress-percent" style="font-weight: 700; color: #6366f1;">0%</span>
          </div>
          <div style="background: #0f172a; height: 10px; border-radius: 5px; overflow: hidden; border: 1px solid #334155;">
            <div id="admin-progress-bar" style="background: #6366f1; height: 100%; width: 0%; transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1);"></div>
          </div>
        </div>
      </div>

      <!-- User Management Section -->
      <div class="admin-panel" style="margin-top: 2rem;">
        <h2 style="margin-bottom: 0.5rem; color: #fff; font-weight: 800;">👨‍💼 Door Pass Control</h2>
        <p style="color: #94a3b8; margin-bottom: 2rem; font-size: 0.9375rem;">Grant or revoke upload permissions for users</p>
        
        <div class="form-group">
          <label for="user-email">Search User by Email</label>
          <input type="text" id="user-email" placeholder="Enter user's email address" onkeyup="searchUsers()">
        </div>
        
        <div id="user-list" class="user-list" style="margin-top: 1.5rem;"></div>
        <div id="no-users" style="text-align: center; padding: 3rem; color: #64748b; background: #0f172a; border-radius: 12px;">
          <p>No matching users found</p>
        </div>
      </div>

      <!-- Stats Section -->
      <div class="admin-panel" style="margin-top: 2rem;">
        <h2 style="margin-bottom: 1.5rem; color: #fff; font-weight: 800;">📊 Platform Statistics</h2>
        <div class="stats-grid">
          <div class="stat-card">
            <h3 id="total-images">0</h3>
            <p>Approved Images</p>
          </div>
          <div class="stat-card" style="border-color: rgba(245, 158, 11, 0.2);">
            <h3 id="pending-images-count" style="color: #f59e0b;">0</h3>
            <p>⏳ Pending Approval</p>
          </div>
          <div class="stat-card">
            <h3 id="total-users">0</h3>
            <p>Total Registered</p>
          </div>
          <div class="stat-card">
            <h3 id="uploaders-count" style="color: #10b981;">0</h3>
            <p>Active Uploaders</p>
          </div>
          <div class="stat-card">
            <h3 id="viewers-count" style="color: #6366f1;">0</h3>
            <p>Basic Viewers</p>
          </div>
        </div>

        <div style="margin-top: 2.5rem;">
          <button class="btn-primary" onclick="showPendingApprovalsAdmin()" style="background: #f59e0b; width: 100%; padding: 1.25rem;">
            📋 Review Pending Approvals
          </button>
        </div>
      </div>
    </div>
  </div>

  <!-- Auth Modal Overlay -->
  <div id="auth-modal" class="modal-overlay" style="display: none;">
    <div class="auth-container">
      <h2>Welcome back</h2>
      <p class="subtitle">Enter your details to manage the platform</p>
      <div class="form-group">
        <label for="auth-email">Email Address</label>
        <input type="email" id="auth-email" placeholder="name@example.com">
      </div>
      <div class="form-group">
        <label for="auth-password">Password</label>
        <input type="password" id="auth-password" placeholder="••••••••">
      </div>
      <button id="auth-submit-btn" class="btn-primary" style="width: 100%; margin-top: 1rem;" onclick="submitAuth()">Sign In</button>
      <div class="auth-links">
        <a href="#" onclick="toggleLoginSignup(event)" style="color: #6366f1; text-decoration: none; font-weight: 600;">Need an account? Sign up</a>
      </div>
      <button class="modal-close-btn" onclick="closeAuthModal()">Skip for now</button>
    </div>
  </div>

  <div id="toast-container"></div>

  <script src="https://www.gstatic.com/firebasejs/9.22.0/firebase-app-compat.js"></script>
  <script src="https://www.gstatic.com/firebasejs/9.22.0/firebase-auth-compat.js"></script>
  <script src="https://www.gstatic.com/firebasejs/9.22.0/firebase-firestore-compat.js"></script>
  <script src="https://www.gstatic.com/firebasejs/9.22.0/firebase-storage-compat.js"></script>
  
  <script src="js/firebase-config.js"></script>
  <script src="js/utils.js"></script>
  <script src="js/auth.js"></script>
  <script src="js/admin.js"></script>
</body>
</html>"""

target_path = os.path.join('..', 'watchman-to-watchmen', 'admin.html')
if os.path.exists(os.path.dirname(target_path)):
    with open(target_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"Successfully updated {target_path}")
else:
    print(f"Directory {os.path.dirname(target_path)} not found. Creating local copy.")
    html_path = 'admin-watchman.html'
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"Successfully created {html_path}")
