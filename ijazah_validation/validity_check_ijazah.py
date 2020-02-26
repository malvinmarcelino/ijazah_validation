import re
import ijazah_validation.functions as functions



# Main function, there are three main steps here
def main(ijazah_path, input_name, input_institution):

    # 1. Read the txt file based on its path
    text = functions.read_txt(ijazah_path)

    # 2. Check validity of the name, institution
    name_validity, name_validity_score, name = functions.check_validity('g', 0.7, input_name, text, show_name=True)
    institution_validity, institution_validity_score, institution = functions.check_validity('g', 0.4, input_institution, text, show_name=True)
    
    return {
                'name': {
                    'result': name,
                    'validity': name_validity,
                    'score': name_validity_score
                },

                'institution': {
                    'result': institution,
                    'validity': institution_validity,
                    'score': institution_validity_score
                },
           }