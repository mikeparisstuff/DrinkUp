DrinkUp
=======

Buy drinks at bars from your smart phone.

This past summer, a friend and I had the idea for a mobile app that would allow people to purchase drinks
from bars directly from their cell phones. I was still working at the time and so I spent some time in the
afternoon and on the weekends creating the origins of what would be the backend for this app. As soon as I 
had something that was beginning to resemble a functional API (Stripe integrationn, User management, transactions, etc.)
I reached out to some local bar owners in Charllottesville to see how they would respond to such a product.
The response I got was one of skepticism not because of the technological implications but becuase of the physical
limitations of the bar staff and POS system.  After discussing solutions to these issues with the owners and researching some
other similar products on the market already, we found that these issues were not special to the bars in the area
and that many others had tried and failed at this already. I am not one to give up when the going gets rough, but
given the huge time outlay that this would require, we decided to table this project for the time being.

However, not all was for naught. This project was a great opportunity for me to get my hands dirty on some Python/Django
code of my own outside of the work place. I created this API myself and got the opportunity to integrate with some
awesome other API's like Stripe and to use some really cool open source projects like Django-Rest-Framework, South, and Swagger.
This now serves me as a reference for some of my new projects and was fun to build regardless of the outcome.

Feel free to check out the source code. At its current state, it is pretty well implemented with Stripe and I had a lot
of fun seeing how real time transactions with my API could automatically be seen on the Stripe dashboard. In addition, there is
pretty extensive documentation that is generated using the Django-Rest-Swagger open source project.
