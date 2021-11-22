<!DOCTYPE html>
<html>
<title>Marketing Home</title>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
<link href="https://fonts.googleapis.com/icon?family=Material+Icons"
<link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Raleway">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
<style>

.myDiv1 {
  margin: auto;
  width: 100%;
  background-color: gray;    
  
}
.myDiv2 {
  margin: auto;
  width: 100%;
  text-align: center;
}





.dropbtn {
  background-color: #04AA6D;
  color: white;
  padding: 16px;
  font-size: 16px;
  border: none;
}

.dropdown {
  position: relative;
  display: inline-block;
}

.dropdown-content {
  display: none;
  position: absolute;
  background-color: #f1f1f1;
  min-width: 160px;
  box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);
  z-index: 1;
}

.dropdown-content a {
  color: black;
  padding: 12px 16px;
  text-decoration: none;
  display: block;
}

.dropdown-content a:hover {background-color: #ddd;}

.dropdown:hover .dropdown-content {display: block;}

.dropdown:hover .dropbtn {background-color: #3e8e41;}






body,h1 {font-family: "Raleway", Arial, sans-serif}
h1 {letter-spacing: 6px}
.w3-row-padding img {margin-bottom: 12px}
</style>
<body class="w3-black">

<!-- !PAGE CONTENT! -->
<div class="w3-content" style="max-width:1500px">

<!-- Header -->
<header class="w3-panel w3-center w3-opacity" style="padding:128px 16px">
  <h1 class="w3-xlarge">Marketing Portal</h1>
  <h1>logged in as {{ user.first_name }} {{ user.last_name }}</h1>
  
  <div class="w3-padding-32">
    <div class="w3-bar w3-border">
      <a href="{% url 'messaging:index2' %}" class="w3-bar-item w3-button">Marketing Home</a>
      <a href="{% url 'messaging:behavior_creation' %}" class="w3-bar-item w3-button">New behavior</a>
      <a href="{% url 'rewards:index' %}" class="w3-bar-item w3-button">Rewards Home</a>
      <a href="{% url 'messaging:analytics' %}" class="w3-bar-item w3-button">Analytics</a>
      
    <div class="w3-dropdown-hover w3-hide-small">
      <button class="w3-padding-large w3-button" title="More">Data Export <i class="fa fa-caret-down"></i></button>     
      <div class="w3-dropdown-content w3-bar-block w3-card-4">
        <a href="{% url 'messaging:transaction_csv' %}" class="w3-bar-item w3-button">Transactions CSV</a>
        <a href="{% url 'messaging:create_csv' %}" class="w3-bar-item w3-button">Customer CSV</a>
        <a href="{% url 'messaging:promo_csv' %}" class="w3-bar-item w3-button">Active Promotions CSV</a>
        <a href="{% url 'messaging:opt_record_csv' %}" class="w3-bar-item w3-button">Opt in Record CSV</a>
        <a href="{% url 'messaging:behavior_csv' %}" class="w3-bar-item w3-button">Behavior CSV</a>
        <a href="{% url 'messaging:message_csv' %}" class="w3-bar-item w3-button">Message CSV</a>
        
      </div>
    </div>
      
     
   <div class="w3-dropdown-hover w3-hide-small">
      <button class="w3-padding-large w3-button" title="More">Data import <i class="fa fa-caret-down"></i></button>     
      <div class="w3-dropdown-content w3-bar-block w3-card-4">
        {% for behavior in behaviors %}
          <a href="{% url 'messaging:get_csv' behavior.id %}" class="w3-bar-item w3-button">{{ behavior.title }}</a>
        {% endfor %}
      </div>
    </div>
     
     
     
     </div>
  </div>
      
     
      
  
     

</header>

<!-- Photo Grid -->
  {% for b in behaviors %}
  <div class="w3-row">
    <div class="w3-col s6 w3-dark-gray w3-center">
   <div class="mydiv2">
    <h4> Plot of transactions from customers who have recieved messaging from the marketing behavior{{b.title}} and messages sent by {{b.title}}</h4>
    
    
        
       
        <p><img src="{{ b.plot_path }}" width="750" height="750"></p>
       
       
    
   </div>
    </div>
    <div class="w3-col s6 w3-light-gray w3-center">
    
          
    
    
    
        
        
        
        <h2> {{ b.getMvalue }} Message data points plotted</h2>
        <h2> {{ b.getTvalue }} Transaction data points plotted</h2>
        <p>X messages sent this week</p>
        <p> X customers who recieved messaging purchased in the last week</p>
        
       
    
    </div>

  </div>
  <p> </p>
  {% endfor %}



  
   
    
  
  
  
<!-- End Page Content -->
</div>



</body>
</html>

