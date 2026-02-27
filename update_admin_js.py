import os

js_content = r"""// Admin panel functionality
let allUsers = [];

// Handle Admin Initialization (called from auth.js when auth state changes)
async function handleAdminInit() {
  const restrictedEl = document.getElementById("admin-restricted");
  const panelEl = document.getElementById("admin-panel-section");
  
  if (!restrictedEl || !panelEl) return;

  const user = auth.currentUser;
  
  if (!user) {
    restrictedEl.style.display = "block";
    panelEl.style.display = "none";
    return;
  }
  
  await updateAdminStatus();
  
  if (window.isCurrentUserAdmin) {
    restrictedEl.style.display = "none";
    panelEl.style.display = "block";
    loadAllUsers();
    loadStatistics();
  } else {
    restrictedEl.style.display = "block";
    panelEl.style.display = "none";
  }
}

// Initial check on load
document.addEventListener("DOMContentLoaded", () => {
  // handleAdminInit will be called by auth.onAuthStateChanged
});

// Load all users
async function loadAllUsers() {
  const userList = document.getElementById("user-list");
  if (!userList) return;
  
  try {
    userList.innerHTML = '<div class="spinner"></div>';
    const snapshot = await db.collection("users").orderBy("createdAt", "desc").get();
    allUsers = [];
    snapshot.forEach(doc => {
      allUsers.push({ id: doc.id, ...doc.data() });
    });
    displayUsers(allUsers);
  } catch (error) {
    console.error("Error loading users:", error);
    userList.innerHTML = '<p style="text-align: center; color: #ef4444;">Failed to load user list.</p>';
  }
}

// Display users
function displayUsers(users) {
  const userList = document.getElementById("user-list");
  const noUsers = document.getElementById("no-users");
  
  if (!userList) return;
  
  if (users.length === 0) {
    userList.innerHTML = "";
    if (noUsers) noUsers.style.display = "block";
    return;
  }
  
  if (noUsers) noUsers.style.display = "none";
  userList.innerHTML = "";
  
  users.forEach(user => {
    const userItem = document.createElement("div");
    userItem.className = "user-item";
    
    const isActuallyAdmin = user.role === "admin";
    const hasDoorPass = user.doorPass || isActuallyAdmin;
    const doorPassStatus = hasDoorPass ? "✅ Access Granted" : "❌ No Access";
    const badgeClass = hasDoorPass ? "badge-verified" : "badge-rejected";
    const joinDate = user.createdAt ? new Date(user.createdAt.toDate()).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' }) : "N/A";
    
    userItem.innerHTML = `
      <div class="user-info">
        <p><strong>${user.email}</strong> ${isActuallyAdmin ? '<span class="image-badge badge-admin" style="margin-left: 0.5rem;">Admin</span>' : ''}</p>
        <div style="display: flex; gap: 0.5rem; align-items: center; margin-top: 0.25rem;">
          <span class="image-badge ${badgeClass}" style="margin: 0; font-size: 0.6rem;">${doorPassStatus}</span>
          <span style="font-size: 0.75rem; color: #64748b;">• Joined ${joinDate}</span>
        </div>
        <p style="font-size: 0.75rem; color: #94a3b8; margin-top: 0.5rem;">
          Total Uploads: <span style="color: #fff; font-weight: 600;">${user.uploadCount || 0}</span>
        </p>
      </div>
      <div>
        ${!isActuallyAdmin ? (
          user.doorPass ? 
          `<button class="btn-delete" style="font-size: 0.75rem; padding: 0.5rem 1rem;" onclick="revokeDoorPassAdmin('${user.id}', '${user.email}')">Revoke Pass</button>` :
          `<button class="btn-primary" style="font-size: 0.75rem; padding: 0.5rem 1rem;" onclick="grantDoorPassAdmin('${user.id}', '${user.email}')">Grant Pass</button>`
        ) : ''}
      </div>
    `;
    
    userList.appendChild(userItem);
  });
}

// Search users
function searchUsers() {
  const searchTerm = document.getElementById("user-email").value.toLowerCase();
  const filtered = allUsers.filter(user => user.email.toLowerCase().includes(searchTerm));
  displayUsers(filtered);
}

// Grant door pass (admin)
async function grantDoorPassAdmin(userId, email) {
  if (!confirm(`Allow ${email} to upload images?`)) return;
  
  if (await grantDoorPass(userId)) {
    showToast("Access granted to " + email, "success");
    loadAllUsers();
    loadStatistics();
  }
}

// Revoke door pass (admin)
async function revokeDoorPassAdmin(userId, email) {
  if (!confirm(`Revoke upload access from ${email}?`)) return;
  
  if (await revokeDoorPass(userId)) {
    showToast("Access revoked from " + email, "warning");
    loadAllUsers();
    loadStatistics();
  }
}

// Load statistics
async function loadStatistics() {
  try {
    const [approvedSnapshot, pendingSnapshot, usersSnapshot] = await Promise.all([
      db.collection("images").where("status", "==", "approved").get(),
      db.collection("images").where("status", "==", "pending").get(),
      db.collection("users").get()
    ]);
    
    if (document.getElementById("total-images")) document.getElementById("total-images").innerText = approvedSnapshot.size;
    if (document.getElementById("pending-images-count")) document.getElementById("pending-images-count").innerText = pendingSnapshot.size;
    if (document.getElementById("total-users")) document.getElementById("total-users").innerText = usersSnapshot.size;
    
    let uploaders = 0;
    usersSnapshot.forEach(doc => {
      if (doc.data().doorPass || doc.data().role === "admin") uploaders++;
    });
    
    if (document.getElementById("uploaders-count")) document.getElementById("uploaders-count").innerText = uploaders;
    if (document.getElementById("viewers-count")) document.getElementById("viewers-count").innerText = usersSnapshot.size - uploaders;
  } catch (error) {
    console.error("Error loading statistics:", error);
  }
}

// Admin Quick Post (Upload)
async function uploadImageAdmin() {
  const user = auth.currentUser;
  if (!user) {
    showToast("Please login first", "warning");
    return;
  }
  
  const title = document.getElementById("admin-image-title").value.trim();
  const description = document.getElementById("admin-image-description").value.trim();
  const file = document.getElementById("admin-image-file").files[0];
  
  if (!title || !file) {
    showToast("Title and image are required", "warning");
    return;
  }
  
  const uploadBtn = document.getElementById("admin-upload-btn");
  const uploadProgress = document.getElementById("admin-upload-progress");
  const progressBar = document.getElementById("admin-progress-bar");
  const progressPercent = document.getElementById("admin-progress-percent");
  
  uploadBtn.disabled = true;
  uploadBtn.innerText = "Processing...";
  uploadProgress.style.display = "block";
  
  try {
    const timestamp = Date.now();
    const filename = `admin/${user.uid}/${timestamp}_${file.name}`;
    const fileRef = storage.ref(filename);
    const uploadTask = fileRef.put(file);
    
    uploadTask.on("state_changed",
      (snapshot) => {
        const progress = (snapshot.bytesTransferred / snapshot.totalBytes) * 100;
        const rounded = Math.round(progress);
        if (progressPercent) progressPercent.innerText = `${rounded}%`;
        if (progressBar) progressBar.style.width = rounded + "%";
      },
      (error) => {
        console.error("Upload error:", error);
        showToast("Upload failed: " + error.message, "error");
        resetUploadFormAdmin();
      },
      async () => {
        const downloadURL = await fileRef.getDownloadURL();
        
        const imageData = {
          title,
          description,
          url: downloadURL,
          uploadedBy: user.email,
          uploadedByUid: user.uid,
          isAdminUpload: true,
          createdAt: new Date(),
          fileSize: file.size,
          fileName: file.name,
          status: "approved",
          verifiedByAdmin: true,
          approvedBy: user.uid,
          approvedAt: new Date()
        };
        
        await db.collection("images").add(imageData);
        
        // Update user count for admin
        const userRef = db.collection("users").doc(user.uid);
        const userDoc = await userRef.get();
        if (userDoc.exists) {
          await userRef.update({
            uploadCount: (userDoc.data().uploadCount || 0) + 1
          });
        }
        
        showToast("Successfully published to gallery!", "success");
        resetUploadFormAdmin();
        loadStatistics();
      }
    );
  } catch (error) {
    console.error("Error uploading image:", error);
    showToast("Error during upload process", "error");
    resetUploadFormAdmin();
  }
}

function resetUploadFormAdmin() {
  const uploadBtn = document.getElementById("admin-upload-btn");
  const uploadProgress = document.getElementById("admin-upload-progress");
  document.getElementById("admin-image-title").value = "";
  document.getElementById("admin-image-description").value = "";
  document.getElementById("admin-image-file").value = "";
  if (uploadBtn) {
    uploadBtn.disabled = false;
    uploadBtn.innerText = "Post to Gallery";
  }
  if (uploadProgress) {
    uploadProgress.style.display = "none";
    document.getElementById("admin-progress-bar").style.width = "0%";
    document.getElementById("admin-progress-percent").innerText = "0%";
  }
}

// Show pending images for admin approval
async function showPendingApprovalsAdmin() {
    window.handleApprove = async (imageId) => {
      if (await verifyImage(imageId)) {
        showToast("Image approved!", "success");
        showPendingApprovalsAdmin();
        loadStatistics();
      }
    };
    
    window.handleReject = async (imageId) => {
      const reason = prompt("Enter rejection reason (optional):");
      if (reason !== null) {
        if (await rejectImage(imageId, reason)) {
          showToast("Image rejected", "warning");
          showPendingApprovalsAdmin();
          loadStatistics();
        }
      }
    };
    
    window.closePendingModal = () => {
      const modal = document.getElementById("pending-approval-modal");
      if (modal) modal.style.display = "none";
    };

    try {
      const snapshot = await db.collection("images")
        .where("status", "==", "pending")
        .orderBy("createdAt", "desc")
        .get();
      
      let modal = document.getElementById("pending-approval-modal");
      if (!modal) {
        modal = document.createElement("div");
        modal.id = "pending-approval-modal";
        modal.className = "modal-overlay";
        document.body.appendChild(modal);
      }
      
      let content = `
        <div class="modal-content" style="max-width: 1100px;">
          <h2 style="font-weight: 800; font-size: 1.5rem; margin-bottom: 0.5rem;">📋 Pending Approval</h2>
          <p style="color: #94a3b8; margin-bottom: 2rem;">Review submissions before they go live.</p>
          <div class="modal-grid" style="display: grid; grid-template-columns: repeat(auto-fill, minmax(240px, 1fr)); gap: 1.5rem;">
      `;
      
      if (snapshot.empty) {
        content += '<div style="grid-column: 1/-1; text-align: center; padding: 4rem 0; color: #64748b;">✓ No pending submissions</div>';
      } else {
        snapshot.forEach(doc => {
          const data = doc.data();
          content += `
            <div class="modal-item" style="background: #0f172a; border-radius: 12px; overflow: hidden; border: 1px solid rgba(255, 255, 255, 0.05);">
              <img src="${data.url}" alt="${data.title}" style="width: 100%; height: 160px; object-fit: cover; cursor: pointer;" onclick="window.open('${data.url}', '_blank')">
              <div style="padding: 1rem;">
                <p style="font-weight: 700; font-size: 0.9375rem; margin-bottom: 0.25rem; color: #fff;">${data.title}</p>
                <p style="font-size: 0.75rem; color: #94a3b8; margin-bottom: 1rem;">By: ${data.uploadedBy}</p>
                <div style="display: flex; gap: 0.5rem;">
                  <button onclick="handleApprove('${doc.id}')" class="btn-primary" style="flex: 1; font-size: 0.75rem; padding: 0.5rem; background: #10b981;">Approve</button>
                  <button onclick="handleReject('${doc.id}')" class="btn-delete" style="flex: 1; font-size: 0.75rem; padding: 0.5rem;">Reject</button>
                </div>
              </div>
            </div>
          `;
        });
      }
      
      content += `
          </div>
          <button onclick="closePendingModal()" class="modal-close-btn" style="margin-top: 2rem;">Back to Dashboard</button>
        </div>
      `;
      
      modal.innerHTML = content;
      modal.style.display = "flex";
      
      modal.addEventListener("click", (e) => {
        if (e.target === modal) closePendingModal();
      });
    } catch (err) {
      console.error(err);
      showToast("Could not load approvals", "error");
    }
}"""

target_path = os.path.join('..', 'watchman-to-watchmen', 'js', 'admin.js')
if os.path.exists(os.path.dirname(target_path)):
    with open(target_path, 'w', encoding='utf-8') as f:
        f.write(js_content)
    print(f"Successfully updated {target_path}")
else:
    print(f"Directory {os.path.dirname(target_path)} not found. Creating local copy.")
    js_path = os.path.join('js', 'admin-watchman.js')
    if not os.path.exists('js'): os.makedirs('js')
    with open(js_path, 'w', encoding='utf-8') as f:
        f.write(js_content)
    print(f"Successfully created {js_path}")
