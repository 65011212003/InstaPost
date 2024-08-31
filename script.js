document.addEventListener('DOMContentLoaded', () => {
    const postsContainer = document.getElementById('posts-container');
    const loadingElement = document.getElementById('loading');

    // Function to fetch posts from the server
    async function fetchPosts() {
        try {
            console.log('Fetching posts...');
            const response = await fetch('/api/posts');
            console.log('Response status:', response.status);
            if (!response.ok) {
                throw new Error('Failed to fetch posts');
            }
            const posts = await response.json();
            console.log('Fetched posts:', posts);
            return posts;
        } catch (error) {
            console.error('Error fetching posts:', error);
            return [];
        }
    }

    // Function to create a post element
    function createPostElement(post) {
        const postElement = document.createElement('div');
        postElement.className = 'bg-white rounded-lg shadow-md overflow-hidden';
        postElement.innerHTML = `
            <img src="${post.image_url}" alt="Post image" class="w-full h-64 object-cover">
            <div class="p-4">
                <p class="text-gray-700">${post.caption}</p>
                <p class="text-gray-500 text-sm mt-2">${new Date(post.created_at).toLocaleString()}</p>
            </div>
        `;
        return postElement;
    }

    // Function to display posts
    async function displayPosts() {
        loadingElement.style.display = 'block';
        const posts = await fetchPosts();
        loadingElement.style.display = 'none';

        console.log('Posts to display:', posts);

        if (posts.length === 0) {
            postsContainer.innerHTML = '<p class="text-center text-gray-500">No posts available.</p>';
        } else {
            postsContainer.innerHTML = ''; // Clear existing posts
            posts.forEach(post => {
                const postElement = createPostElement(post);
                postsContainer.appendChild(postElement);
            });
        }
    }

    // Call the displayPosts function when the page loads
    displayPosts();
});