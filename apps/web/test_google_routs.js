//hecho con ia
const API_KEY = process.env.GOOGLE_ROUTS_API_KEY;
fetch(`https://routes.googleapis.com/directions/v2:computeRoutes`, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'X-Goog-Api-Key': API_KEY,
    'X-Goog-FieldMask': 'routes.distanceMeters,routes.duration'
  },
  body: JSON.stringify({
    origin: { address: "Providencia, Santiago, Chile" },
    destination: { address: "Santiago Centro, Chile" },
    travelMode: "DRIVE"
  })
})
.then(res => res.json())
.then(data => console.log("Google Routes OK:", data))
.catch(err => console.error(err));