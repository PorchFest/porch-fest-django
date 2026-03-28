function itineraryHandler() {
    return {
        message: '',

        async addPerformance(performanceId) {
			console.log(performanceId)
            try {
                // const response = await axios.get("/api/porches/porch-map", {
                //     params: data
                // })
                const response = await fetch(`/api/${performanceId}/add`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        // 'X-CSRFToken': this.getCSRFToken(),
                    },
                    // body: JSON.stringify({
                    //     performance_id: performanceId
                    // })
                });

                if (response.ok) {
                    this.message = "Added to itinerary ✅";
                } else {
                    this.message = "Something went wrong ❌";
                }
            } catch (e) {
                this.message = "Network error ❌";
            }
        },

        getCSRFToken() {
            return document.cookie
                .split('; ')
                .find(row => row.startsWith('csrftoken='))
                ?.split('=')[1];
        }
    }
}