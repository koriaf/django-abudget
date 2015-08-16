<div class='col-lg-3'>
    <div class="panel panel-default">
        <div class="panel-heading">
            <i class="fa fa-thumb-tack"></i> Filter by
        </div>
        <div class="panel-body">
            <form action="{% url 'money:update_filter' %}" method='post'>
                {% csrf_token %}
                <input type='hidden' name='redirect_to' value="{{ request.META.PATH_INFO }}" />
                <select name='date' class='form-control'>
                    <option value='this_month' {% if request.session.filter_by.date == 'this_month' %}selected{% endif %}>This month</option>
                    <option value='prev_month' {% if request.session.filter_by.date == 'prev_month' %}selected{% endif %}>Previous month</option>
                    <option value='from_the_beginning' {% if request.session.filter_by.date == 'from_the_beginning' %}selected{% endif %}>From the beginning</option>
                    <option value='date_custom' {% if request.session.filter_by.date == 'date_custom' %}selected{% endif %}>Custom range</option>
                </select>

                <div class="input-group">
                  <input type="text" class="form-control" placeholder="from date (empty for today)" value="{{ request.session.filter_by.date_from|default:'' }}" name="date_from">
                  <input type="text" class="form-control" placeholder="to date (empty for today)" value="{{ request.session.filter_by.date_to|default:'' }}" name="date_to">
                </div>

                <button type='submit' class='btn btn-primary big-button'>Apply</button>
            </form>
        </div>
    </div>
</div>
