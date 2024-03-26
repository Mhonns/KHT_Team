const form = document.getElementById('village-url-form');
console.log('Form:', form);

form.addEventListener('submit', async (event) => {
  event.preventDefault(); // Prevent default form submission
  console.log('Form submitted!');

  const villageName = document.getElementById('village_name').value;
  const url = document.getElementById('url').value;
  const imageUrl = document.getElementById('image_url').value;
  const articleTitle = document.getElementById('article_title').value || ''; // Set to empty string if null
  const postedDate = document.getElementById('posted_date').value || ''; // Set to empty string if null

  // Validate the form data
  const data = {
    village_name: villageName,
    url: url,
    image_url: imageUrl,
    article_title: articleTitle,
    posted_date: postedDate
  };

  try {
    const response = await fetch('https://172.105.120.121:443/api/post/village_url', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });

    if (response.ok) {
      const jsonResponse = await response.json();
      //convert JSON to string
      alert(JSON.stringify(jsonResponse));
      console.log('Response:', jsonResponse);
    } else {
      alert('Error creating village URL: ' + await response.text());
    }
  } catch (error) {
    console.error('Error:', error);
    alert('An error occurred. Please try again later.');
  }
});
