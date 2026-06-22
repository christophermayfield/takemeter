Community: I picked r/unpopularopinion

Labels: 
    - hot_take: a strong, often controversial opinion, may also make mock someone 

    https://www.reddit.com/r/unpopularopinion/comments/1u6wyuc/i_believe_wicked_was_completely_ruined_because_it/

    https://www.reddit.com/r/unpopularopinion/comments/1u5xxrj/uniforms_should_be_mandatory_at_any_job/

    - analytical: general argument - may provide evidence or reasoning


    https://www.reddit.com/r/unpopularopinion/comments/1u63a2o/its_ok_to_like_well_done_steak/

    https://www.reddit.com/r/unpopularopinion/comments/1u6suix/waiting_longer_to_have_sex_would_probably_save_a/


    -nostalgia_maxxing - longing for the past, making allures to a greater time, may complain about the present

    https://www.reddit.com/r/unpopularopinion/comments/1tom4dh/going_out_in_your_30s_is_mostly_people_pretending/

    https://www.reddit.com/r/unpopularopinion/comments/1u3gyxo/the_vuvuzelas_in_the_2010_world_cup_were_really/

    

    Hard Edge Cases - The tough cases will be between hot_take and analytical, someimes these tend to be tough because a hot_take can be mixed with an analytical argument but then have some reasoning. I will try my best to use some judgement on that, maybe use a python library such as Spacy to help with that. 

    Data Collection Plan - I tend to use a web scraper to get all the titles using the Reddit API, then I will use a python to seperate them into train and test cases. 

    Evaluation metrics -  Accuracy, Confusion Matrix, and F1 score. 

    Definition of Success - an accuracy of roughly 85% success. 

    

AI Tool Plan 
Label stress-testing 
 hot_take: a strong, often controversial opinion, may also make mock someone else's opinion, or be a general statement that is not necessarily true. 
 edge case: using a fact that may be made up in a way to be sardonic 

 analytical: general argument - may provide evidence or reasoning to support the claim. 
 edge case: when someone is trying to one-up someone else, or is being sarcastic, or is making a joke, or is making a statement that is not necessarily true. 

 nostalgia_maxxing - longing for the past, making allures to a greater time, may complain about the present
 edge case: when someone is saying something about the past that doesn't necessarily apply. 

Annotation Assitance
Yes, using pandas 

Failure Analysis 
I'll look for obvious misalignment of labels. i'll steer the LLM toward the correct labeling scheme if needed. 



{
  "baseline_accuracy": 0.6765,
  "finetuned_accuracy": 0.5588,
  "improvement": -0.1176,
  "test_set_size": 34,
  "label_map": {
    "analytical": 0,
    "hot_take": 1,
    "nostalgia_maxxing": 2
  },
  "model": "distilbert-base-uncased"
}


![My Image](confusion_matrix.png)