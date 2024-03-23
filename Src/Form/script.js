const form = document.getElementById('village-url-form');
const village_url_model = {
  village_name: '', // Assume villageName is a string
  url: '', // Assume url is an array of strings
  image_url: '', // Assume imageUrl is a string
  article_title: '', // Assume articleTitle is a string
  posted_date:  ''
};


form.addEventListener('submit', async (event) => {
  event.preventDefault(); // Prevent default form submission

  const villageName = document.getElementById('village_name').value;
  const url1 = document.getElementById('url').value;
  const url2 = document.getElementById('image_url').value;
  const articleTitle = document.getElementById('article_title').value || ''; // Set to empty string if null
  const postedDate = document.getElementById('posted_date').value || ''; // Set to empty string if null

  // Validate the form data
  const data = {
    village_name: villageName,
    url: url1,
    image_url: url2,
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
      alert('Village URL created successfully!');
      console.log('Success:', await response.json());
      // Optionally, clear the form or redirect to another page
    } else {
      alert('Error creating village URL: ' + await response.text());
    }
  } catch (error) {
    console.error('Error:', error);
    alert('An error occurred. Please try again later.');
  }
});
