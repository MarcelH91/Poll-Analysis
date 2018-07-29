from django.db import models
from django.utils import timezone
import datetime
from django_pandas.io import read_frame
import matplotlib.pyplot as plt
from io import BytesIO
import base64

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def results_table(self):
        df = read_frame(self.choice_set.all(), fieldnames=[         'choice_text', 'votes'])
        return df.to_html()

    def results_plot(self):
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        df = read_frame(self.choice_set.all())
        df.plot(x='choice_text', y='votes', kind='bar', ax=ax)
        
        #save figure as bytes
        io = BytesIO() 
        fig.savefig(io, format='png')
        
        #decode bytes back to String
        data = base64.encodebytes(io.getvalue()).decode('UTF-8')
        
        #fill data into html-img
        html = '<img src="data:image/png;base64,{}" width="50%"/>'
        return html.format(data)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

