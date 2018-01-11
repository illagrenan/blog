# blog

[![CircleCI](https://circleci.com/gh/illagrenan/blog.svg?style=svg&circle-token=fe748d519afa265654a525658b1a4088dfaefbce)](https://circleci.com/gh/illagrenan/blog)


            # https://serverfault.com/questions/725562/recursively-changing-the-content-type-for-files-of-a-given-extension-on-amazon-s
            # aws s3 cp --include "*" \
            #          --content-type="text/html" \
            #          --metadata-directive="REPLACE" \
            #          --recursive s3://${S3_BUCKET_NAME}/posts/ s3://${S3_BUCKET_NAME}/posts/
